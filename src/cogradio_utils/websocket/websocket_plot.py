import json
import numpy as np
from .websocket import ServerProtocol
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

    data_buffer = "[]"

    def __init__(self):
        ServerProtocol.__init__(self)

    @inlineCallbacks
    def pushData(self):
        if self.queue.empty() == False:
            data = self.queue.get().tolist()
            self.data_buffer = json.dumps(data).encode('utf8')

        yield sleep(0.05)
        self.sendMessage(self.data_buffer)

    def onOpen(self):
        print("WebSocket connection open.")
        self.pushData()

    def onMessage(self, payload, isBinary):
        self.pushData()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


class WebSocketServerPlotFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, url, queue):
        self._queue = queue
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.queue = self._queue
        protocol.factory = self
        return protocol
