import json
import time
import Pyro4
from multiprocessing import Queue
from twisted.internet import defer
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol


class ServerProtocolDash(WebSocketServerProtocol):

    """WebSocket protocol for processing configuration data"""

    def __init__(self):
        self.client_address = ''
        self.timestamp = time.time()
        self.settings = Pyro4.Proxy("PYRONAME:cg.settings")
        WebSocketServerProtocol.__init__(self)

    def onOpen(self):
        print("WebSocket connection open.")

        def update():
            if self.factory.content.update_timestamp != self.timestamp and \
                    self.factory.content.update_client != self.client_address:
                self.timestamp = self.factory.content.update_timestamp
                update_code = self.factory.content.update_eval()
                self.sendMessage(json.dumps(update_code))

            self.factory.reactor.callLater(0.01, update)

        update()

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))
        self.client_address = request.peer

    def onMessage(self, payload, isBinary):
        data = json.loads(payload)
        self.factory.content.set_by_uuid(data['id'], data['value'], self.client_address)
        values = self.factory.content.values
        self.settings.update(values)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


class WebSocketServerDashFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, url, content):
        self.content = content
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.factory = self
        return protocol
