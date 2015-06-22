import json
import spectral as spec
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol


class ServerProtocolData(WebSocketServerProtocol):

    """WebSocket protocol for pushing plot data"""

    SRC_DATA = 'src_data'
    REC_DATA = 'rec_data'
    DET_DATA = 'det_data'
    datatypes = (SRC_DATA, REC_DATA, DET_DATA)

    sample_freq = 10e6
    center_freq = 2.4e9

    def __init__(self):
        self.settings = spec.supervisor.get_settings_object()

        WebSocketServerProtocol.__init__(self)

    def pushData(self, request):
        container = self.factory.dequeue(request)
        self.update_options()

        if container:
            message = PlotDataContainer(self.sample_freq, self.center_freq, container.dtype, container.data)
            self.sendMessage(message.encode())

    def onOpen(self):
        print("WebSocket connection open.")

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        self.pushData(payload)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def update_options(self):
        options = self.settings.read()
        for key, value in options.items():
            if key == 'center_freq':
                self.center_freq = value * 1e9
            elif hasattr(self, key):
                setattr(self, key, value)


class ServerProtocolDataFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, url, src_queue, rec_queue, det_queue, sample_freq):
        self.sample_freq = sample_freq
        self.queues = {
            ServerProtocolData.SRC_DATA: src_queue,
            ServerProtocolData.REC_DATA: rec_queue,
            ServerProtocolData.DET_DATA: det_queue
        }
        self.buffers = {
            ServerProtocolData.SRC_DATA: None,
            ServerProtocolData.REC_DATA: None,
            ServerProtocolData.DET_DATA: None
        }

        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.sample_freq = self.sample_freq
        protocol.factory = self
        return protocol

    def dequeue(self, request):
        if request not in self.buffers:
            raise ValueError("Invalid request: '{}'".format(request))

        item = self.queues[request].dequeue()
        if item is not None:
            self.buffers[request] = item

        return self.buffers[request]


class PlotDataContainer:

    """Class containing the data that should be sent to client for plotting"""

    def __init__(self, sample_freq, center_freq, dtype, data):
        self.sample_freq = sample_freq
        self.center_freq = center_freq
        self.dtype = dtype

        if not isinstance(data, list):
            self.data = data.tolist()
        else:
            self.data = data

    def encode(self):
        obj = dict(self.__dict__)
        return json.dumps(obj).encode('utf8')


class WebsocketDataContainer:

    """Class containing the data that is used by the websocket for plotting"""

    def __init__(self, dtype, data):
        if dtype not in ServerProtocolData.datatypes:
            raise ValueError("Invalid datatype passed to websocket datacontainer")

        self.dtype = dtype
        self.data = data

    def enqueue(self, queue):
        queue.queue(self)
