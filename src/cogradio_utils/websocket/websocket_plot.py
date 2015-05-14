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
    average = False
    delay = 0.05
    N = 10

    REQUEST_DATA = 0

    def __init__(self):
        self.series = deque(maxlen=self.N)
        ServerProtocol.__init__(self)

    @inlineCallbacks
    def pushData(self):
        if self.queue.empty() == False:
            self.data_buffer = self.queue.get()

        if self.average:
            self.makeAverage()

        # Slow the loop down a bit.
        yield sleep(0.05)
        self.sendMessage(self.data_buffer.encode())

    def onOpen(self):
        print("WebSocket connection open.")
        self.pushData()

    def onMessage(self, payload, isBinary):
        last_options = None
        while self.opt.poll():
            last_options = self.opt.recv()

        if last_options is not None:
            self.average = last_options['average']

        if int(payload) == self.REQUEST_DATA:
            self.pushData()
        else:
            print("Unsupported message.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def makeAverage(self):
        if len(self.series) == self.N:
            self.series.popleft()

        self.series.append(self.data_buffer.data)

        if len(self.series) == self.N:
            a = np.asarray(list(self.series))
            self.data_buffer.data = np.average(a, axis=0).tolist()


class WebSocketServerPlotFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, url, queue, opt):
        self._queue = queue
        self._opt = opt
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.queue = self._queue
        protocol.opt = self._opt
        protocol.factory = self
        return protocol


class PlotDataContainer:

    """Class containing the data that should be sent to client for plotting"""

    def __init__(self, sample_freq, data):
        self.sample_freq = sample_freq
        self.data = data.tolist()

    def encode(self):
        obj = dict(sample_freq=self.sample_freq, data=self.data)
        return json.dumps(obj).encode('utf8')
