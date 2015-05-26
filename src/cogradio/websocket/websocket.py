import json
import cogradio as cg
# import numpy as np
from multiprocessing import Queue
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol


class ServerProtocolPlot(WebSocketServerProtocol):

    """WebSocket protocol for pushing plot data"""

    src_buffer = None
    rec_buffer = None
    det_buffer = None

    src_queue = None
    rec_queue = None
    det_queue = None

    SRC_DATA = 'src_data'
    REC_DATA = 'rec_data'
    DET_DATA = 'det_data'

    sample_freq = 10e6
    center_freq = 2.41e9

    def __init__(self):
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
        if request == self.SRC_DATA:
            if not self.src_queue.empty():
                self.src_buffer = self.src_queue.get()

            return self.src_buffer

        if request == self.REC_DATA:
            if not self.rec_queue.empty():
                self.rec_buffer = self.rec_queue.get()

            return self.rec_buffer

        if request == self.DET_DATA:
            if not self.det_queue.empty():
                self.det_buffer = self.det_queue.get()

            return self.det_buffer

        raise ValueError("Invalid request: '{}'".format(request))


class WebSocketServerPlotFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, **kwargs):
        url = kwargs.pop('url')
        self.protocol_params = kwargs
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        for key, value in self.protocol_params.items():
            setattr(protocol, key, value)
        protocol.factory = self
        return protocol


class PlotDataContainer:

    """Class containing the data that should be sent to client for plotting"""

    def __init__(self, sample_freq, center_freq, dtype, data):
        self.sample_freq = sample_freq
        self.center_freq = center_freq
        self.dtype = dtype
        self.data = data.tolist()

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
