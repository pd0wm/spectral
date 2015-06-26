import json
import spectral as spec
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol


class ServerProtocolData(WebSocketServerProtocol):

    """
    WebSocket protocol for processing plot data. The protocol describes
    how various connection events should be handled so that each connected
    client may receive the most recent data from :mod:spectral.core.
    """

    SRC_DATA = 'src_data'
    REC_DATA = 'rec_data'
    DET_DATA = 'det_data'
    datatypes = (SRC_DATA, REC_DATA, DET_DATA)

    sample_freq = 10e6
    center_freq = 2.4e9

    def __init__(self):
        self.settings = spec.supervisor.get_settings_object()

        WebSocketServerProtocol.__init__(self)

    def pushData(self, request):
        """
        Pushes the requested data to the client.

        Args:
            request: The requested data type.
        """
        container = self.factory.dequeue(request)
        self.update_options()

        if container:
            message = PlotDataContainer(self.sample_freq, self.center_freq, container.dtype, container.data)
            self.sendMessage(message.encode())

    def onOpen(self):
        """
        Handles the WebSocket onOpen event. Fired when the connection is
        established.
        """
        print("WebSocket connection open.")

    def onConnect(self, request):
        """
        Handles the WebSocket onConnect event. Fired when the client starts to
        connect.

        Args:
            request: The request object.
        """
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        """
        Handles the connection onMessage event. Fired when the server receives
        a message. Will push the requested data to the requesting client.

        Args:
            payload: The message content.
            isBinary: Whether the payload is binary encoded.
        """
        self.pushData(payload)

    def onClose(self, wasClean, code, reason):        
        """
        Handles the connection onClose event. Fired when the connection is
        closed.

        Args:
            wasClean: Whether the connection closed cleanly.
            code: The closing code.
            reason: The reason for closing the connection.
        """
        print("WebSocket connection closed: {}".format(reason))

    def update_options(self):
        """
        Updates the local settings using the :class:Settings class.
        """
        options = self.settings.read()
        for key, value in options.items():
            if key == 'center_freq':
                self.center_freq = value * 1e9
            elif hasattr(self, key):
                setattr(self, key, value)


class ServerProtocolDataFactory(WebSocketServerFactory):

    """
    Factory for creating :class:ServerProtocolData instances.

    Args:
        url: The url to start the WebSocket server on.
        src_queue: The queue to read source data from.
        rec_queue: The queue to read reconstruction data from.
        det_queue: The queue to read detection data from.
        sample_freq: The sample frequency for all data.
    """

    def __init__(self, url, src_queue, rec_queue, det_queue, sample_freq):
        self.sample_freq = sample_freq
        self.queues = {
            ServerProtocolData.SRC_DATA: src_queue,
            ServerProtocolData.REC_DATA: rec_queue,
            ServerProtocolData.DET_DATA: det_queue
        }
        self.buffers = {
            ServerProtocolData.SRC_DATA: None,
            ServerProtocolData.REC_DATA: None,
            ServerProtocolData.DET_DATA: None
        }

        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        """
        Builds a :class:ServerProtocolData instance.

        Args:
            addr: (unused) The address of the client for this protocol.
        """
        protocol = self.protocol()
        protocol.sample_freq = self.sample_freq
        protocol.factory = self
        return protocol

    def dequeue(self, request):
        """
        Receive the latest data from the given queue and put it in the
        correct buffer.

        Args:
            request: The requested data type.
        """
        if request not in self.buffers:
            raise ValueError("Invalid request: '{}'".format(request))

        item = self.queues[request].dequeue()
        if item is not None:
            self.buffers[request] = item

        return self.buffers[request]


class PlotDataContainer:

    """
    Class containing the data that should be sent to client for plotting.

    Args:
        sample_freq: The sample frequency for the data.
        center_freq: The center_freq for the data.
        dtype: The datatype.
        data: The data itself.
    """

    def __init__(self, sample_freq, center_freq, dtype, data):
        self.sample_freq = sample_freq
        self.center_freq = center_freq
        self.dtype = dtype

        if not isinstance(data, list):
            self.data = data.tolist()
        else:
            self.data = data


    def encode(self):
        """
        Returns a JSON dump of itself, UTF-8 encoded.

        Returns:
            The encoded string.
        """
        obj = dict(self.__dict__)
        return json.dumps(obj).encode('utf8')


class WebsocketDataContainer:

    """
    Class containing the data that is used by the websocket for plotting.

    Args:
        dtype: The datatype.
        data: The data itself.
    """

    def __init__(self, dtype, data):
        if dtype not in ServerProtocolData.datatypes:
            raise ValueError("Invalid datatype passed to websocket datacontainer")

        self.dtype = dtype
        self.data = data

    def enqueue(self, queue):
        """
        Enqueues itself in the given queue.

        Args:
            queue: The queue to enqueue in.
        """
        queue.queue(self)
