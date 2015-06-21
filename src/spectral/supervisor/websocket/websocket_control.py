import json
import spectral as spec
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol


class ServerProtocolControl(WebSocketServerProtocol):

    """
    WebSocket protocol for processing configuration data. The protocol describes
    how various connection events should be handled so that each connected
    is able to modify system settings and gets notified of changes that other
    clients make.
    """

    factory = None

    def __init__(self):
        self.settings = spec.supervisor.get_settings_object()
        WebSocketServerProtocol.__init__(self)

    def onOpen(self):
        """
        Handles the WebSocket onOpen event. Fired when the connection is
        established. The protocol will register itself with the factory and
        push a list of current settings to the client.
        """
        print "WebSocket connection open."
        self.factory.register(self)

        # Push initial settings to client
        settings = self.settings.read()
        settings['settings'] = True
        self.sendMessage(json.dumps(settings).encode('utf8'))

    def onConnect(self, request):
        """
        Handles the WebSocket onConnect event. Fired when the client starts to
        connect.
        """
        print "Client connecting: {}".format(request.peer)

    def onMessage(self, payload, isBinary):
        """
        Handles the connection onMessage event. Fired when the server receives
        a message. The server will decode the message, update the new settings
        and relay it to all other clients.
        """
        data = json.loads(payload)
        self.settings.update({data['key']: data['value']})
        self.factory.relay(self, payload)

    def onClose(self, wasClean, code, reason):
        """
        Handles the connection onClose event. Fired when the connection is
        closed.
        """
        print "WebSocket connection closed: {}".format(reason)
        self.factory.unregister(self)


class ServerProtocolControlFactory(WebSocketServerFactory):

    """
    Factory for creating ServerProtocolControl instances.

    Args:
    url: The url to start the WebSocket server on.
    """

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        """
        Registers the given client, so that it will receive updated settings.

        Args:
        client: The protocol instance of the client that connected.
        """
        if client not in self.clients:
            print "Registered client {}".format(client.peer)
            self.clients.append(client)

    def unregister(self, client):
        """
        Registers the given client, so that it will stop receiving updated
        settings.

        Args:
        client: The :class:ServerProtocolControl instance of the client that
        connected.
        """
        if client in self.clients:
            print "Unregistered client {}".format(client.peer)
            self.clients.remove(client)

    def relay(self, client, msg):
        """
        Relays the given message to all registered clients.

        Args:
        client: The client that originally received the message to relay.
        msg: The message to relay.
        """
        for c in self.clients:
            if c is not client:
                c.sendMessage(msg.encode('utf8'))

    def buildProtocol(self, addr):
        """
        Builds a :class:ServerProtocolControl instance.

        Args:
        addr: (unused) The address of the client for this protocol.
        """
        protocol = self.protocol()
        protocol.factory = self
        return protocol
