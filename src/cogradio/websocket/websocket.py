import json
import cogradio as cg
from multiprocessing import Queue
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol


class ServerProtocolPlot(WebSocketServerProtocol):

    """WebSocket protocol for pushing plot data"""

    queue = None

    SRC_DATA = 'src_data'
    REC_DATA = 'rec_data'
    DET_DATA = 'det_data'

    sample_freq = 10e6
    center_freq = 2.41e9

    def __init__(self):
        self.buffer = {
            self.SRC_DATA: None,
            self.REC_DATA: None,
            self.DET_DATA: None
        }
        WebSocketServerProtocol.__init__(self)

    def pushData(self, request):
        container = self.dequeue(request)
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
        options = None
        while self.opt.poll():
            options = self.opt.recv()

        if options:
            for key, value in options.items():
                if key == 'center_freq':
                    self.center_freq = value * 1e6
                elif hasattr(self, key):
                    setattr(self, key, value)

    def dequeue(self, request):
        if request not in self.buffer:
            raise ValueError("Invalid request: '{}'".format(request))

        if not self.queue[request].empty():
            self.buffer[request] = self.queue[request].get()

        return self.buffer[request]


class WebSocketServerPlotFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, **kwargs):
        url = kwargs.pop('url')
        self.protocol_params = kwargs
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.queue = {
            ServerProtocolPlot.SRC_DATA: self.protocol_params['src_queue'],
            ServerProtocolPlot.REC_DATA: self.protocol_params['rec_queue'],
            ServerProtocolPlot.DET_DATA: self.protocol_params['det_queue']
        }
        protocol.center_freq = self.protocol_params['center_freq']
        protocol.sample_freq = self.protocol_params['sample_freq']
        protocol.opt = self.protocol_params['opt']
        protocol.factory = self
        return protocol


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
        if (dtype != ServerProtocolPlot.SRC_DATA) and \
                (dtype != ServerProtocolPlot.REC_DATA) and \
                (dtype != ServerProtocolPlot.DET_DATA):
            raise ValueError("Invalid datatype passed to websocket datacontainer")

        self.dtype = dtype
        self.data = data

    def enqueue(self, queue):
        if queue.full():
            queue.get()

        queue.put_nowait(self)
