import json
import Pyro4
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol


class ServerProtocolControl(WebSocketServerProtocol):

    """WebSocket protocol for processing configuration data"""

    factory = None

    def __init__(self):
        self.settings = Pyro4.Proxy("PYRONAME:cg.settings")
        WebSocketServerProtocol.__init__(self)

    def onOpen(self):
        print "WebSocket connection open."
        self.factory.register(self)

        # Push initial settings to client
        settings = self.settings.read()
        settings['settings'] = True
        self.sendMessage(json.dumps(settings).encode('utf8'))

    def onConnect(self, request):
        print "Client connecting: {}".format(request.peer)

    def onMessage(self, payload, isBinary):
        data = json.loads(payload)
        self.settings.update({data['key']: data['value']})
        self.factory.relay(self, payload)

    def onClose(self, wasClean, code, reason):
        print "WebSocket connection closed: {}".format(reason)
        self.factory.unregister(self)


class ServerProtocolControlFactory(WebSocketServerFactory):

    """Factory for creating ServerProtocolControl instances"""

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            print "Registered client {}".format(client.peer)
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print "Unregistered client {}".format(client.peer)
            self.clients.remove(client)

    def relay(self, client, msg):
        for c in self.clients:
            if c is not client:
                c.sendMessage(msg.encode('utf8'))

    def buildProtocol(self, addr):
        protocol = self.protocol()
        protocol.factory = self
        return protocol
