import json
import numpy as np
from .websocket import ServerProtocol
from collections import deque
from multiprocessing import Queue
from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from autobahn.twisted.websocket import WebSocketServerFactory


def sleep(delay):
    d = Deferred()
    reactor.callLater(delay, d.callback, None)
    return d


class ServerProtocolPlot(ServerProtocol):

    """WebSocket protocol for pushing plot data"""

    queue = None
    data_buffer = None
    delay = 0.05

    sample_freq = 10e6
    center_freq = 2.41e9

    REQUEST_DATA = 0

    def __init__(self):
        ServerProtocol.__init__(self)

    def pushData(self):
        if self.queue.empty() == False:
            self.data_buffer = self.queue.get()

        options = None
        while self.opt.poll():
            options = self.opt.recv()
        if options:
            self.parse_options(options)

        message = PlotDataContainer(self.sample_freq, self.center_freq, self.data_buffer)
        self.sendMessage(message.encode())

    def onOpen(self):
        print("WebSocket connection open.")
        self.pushData()

    def onMessage(self, payload, isBinary):
        if int(payload) == self.REQUEST_DATA:
            self.pushData()
        else:
            print("Unsupported message.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def parse_options(self, options):
        print options
        for key, value in options.items():
            if key == 'center_freq':
                self.center_freq = value * 1e6
            elif hasattr(self, key):
                setattr(self, key, value)


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

    def __init__(self, sample_freq, center_freq, data):
        self.sample_freq = sample_freq
        self.center_freq = center_freq
        self.data = data.tolist()

    def encode(self):
        obj = dict(self.__dict__)
        return json.dumps(obj).encode('utf8')
