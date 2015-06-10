import json
import cogradio as cg
import Pyro4
from multiprocessing import Queue
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol


class ServerProtocolPlot(WebSocketServerProtocol):

    """WebSocket protocol for pushing plot data"""

    SRC_DATA = 'src_data'
    REC_DATA = 'rec_data'
    DET_DATA = 'det_data'

    sample_freq = 10e6
    center_freq = 2.4e9

    def __init__(self):
        self.settings = Pyro4.Proxy("PYRONAME:cg.settings")

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


class WebSocketServerPlotFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, url, src_queue, rec_queue, det_queue, sample_freq):
        self.sample_freq = sample_freq
        self.queues = {
            ServerProtocolPlot.SRC_DATA: src_queue,
            ServerProtocolPlot.REC_DATA: rec_queue,
            ServerProtocolPlot.DET_DATA: det_queue
        }
        self.buffers = {
            ServerProtocolPlot.SRC_DATA: None,
            ServerProtocolPlot.REC_DATA: None,
            ServerProtocolPlot.DET_DATA: None
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

        if not self.queues[request].empty():
            self.buffers[request] = self.queues[request].get()

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
