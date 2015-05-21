from autobahn.twisted.websocket import WebSocketServerProtocol


class ServerProtocol(WebSocketServerProtocol):

    """Parent object for a WebSocket server protocol"""

    def __init__(self):
        WebSocketServerProtocol.__init__(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print('Received binary message.')
        else:
            print('Received message: {}'.format(payload))

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
