import json
import time
import Pyro4
from multiprocessing import Queue
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol


settings = Pyro4.Proxy("PYRONAME:cg.settings")


class ServerProtocolDash(WebSocketServerProtocol):

    """WebSocket protocol for processing configuration data"""

    def __init__(self):
        WebSocketServerProtocol.__init__(self)

    def onOpen(self):
        print("WebSocket connection open.")
        timestamp = time.time()

        def update():
            if self.content.poll_updates() or self.content.timestamp != timestamp:
                timestamp = self.content.timestamp
                update_code = self.content.update_eval()
                self.sendMessage(json.dumps(update_code))
            self.factory.reactor.callLater(0.05, update)

        update()

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        data = json.loads(payload)
        print data
        self.content.set_by_uuid(data['id'], data['value'])
        settings.update(self.content.values)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


class WebSocketServerDashFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolPlot instances"""

    def __init__(self, **kwargs):
        url = kwargs.pop('url')
        self.protocol_params = kwargs
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.factory = self
        protocol.content = self.protocol_params['content']
        return protocol
