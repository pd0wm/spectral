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

    def __init__(self):
        ServerProtocol.__init__(self)

    @inlineCallbacks
    def onOpen(self):
        print("WebSocket connection open.")

        while self.state == self.STATE_OPEN:
            data = self.queue.get_nowait().tolist()
            encode = json.dumps(data).encode('utf8')
            print(encode)
            self.sendMessage(encode)
            yield sleep(0.5)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


class WebSocketServerPlotFactory(WebSocketServerFactory):

    def __init__(self, url, queue):
        self._queue = queue
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.queue = self._queue
        protocol.factory = self
        return protocol
