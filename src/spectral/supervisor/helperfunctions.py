import spectral as spec
import sys
import Pyro4
from twisted.python import log
from twisted.internet import reactor


def get_settings_object():
    """
    Returns the Pyro4 proxy for the core settings.

    Returns:
        A Pyro4 Proxy instance.
    """
    return Pyro4.Proxy("PYRONAME:sc.settings")


def send_to_websocket(queue, data, dtype):
    """
    Wraps the data in an :class:WebsocketDataContainer and enqueues it for 
    the WebSocket.

    Args:
        queue: The queue to put the data in.
        data: The data itself.
        dtype: The datatype.
    """
    container = spec.supervisor.websocket.WebsocketDataContainer(dtype, data)
    container.enqueue(queue)


def websocket_control(port):
    """
    Starts the WebSocket in charge of handling system settings.

    Args:
        port: The port to start the server on.
    """
    log.startLogging(sys.stdout)
    factory = spec.supervisor.websocket.ServerProtocolControlFactory(url="ws://localhost:{}".format(port))
    factory.protocol = spec.supervisor.websocket.ServerProtocolControl
    reactor.listenTCP(port, factory)
    reactor.run()


def websocket_data(port, src_queue, rec_queue, det_queue, sample_freq):
    """
    Starts the WebSocket in charge of handling plot data.

    Args:
        port: The port to start the server on.
        src_queue: The queue to read source data from.
        rec_queue: The queue to read reconstruction data from.
        det_queue: The queue to read detection data from.
        sample_freq: The sample frequency for all data.
    """
    log.startLogging(sys.stdout)
    factory = spec.supervisor.websocket.ServerProtocolDataFactory(url="ws://localhost:{}".format(port),
                                                                  src_queue=src_queue,
                                                                  rec_queue=rec_queue,
                                                                  det_queue=det_queue,
                                                                  sample_freq=sample_freq,
                                                                  )
    factory.protocol = spec.supervisor.websocket.ServerProtocolData
    reactor.listenTCP(port, factory)
    reactor.run()
