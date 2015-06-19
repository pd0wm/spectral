import spectral_supervisor as ss
import sys
import Pyro4
from twisted.python import log
from twisted.internet import reactor


def get_settings_object():
    return Pyro4.Proxy("PYRONAME:sc.settings")


def send_to_websocket(queue, data, dtype):
    container = ss.websocket.WebsocketDataContainer(dtype, data)
    container.enqueue(queue)


def websocket_control(port):
    log.startLogging(sys.stdout)
    factory = ss.websocket.ServerProtocolControlFactory(url="ws://localhost:{}".format(port))
    factory.protocol = ss.websocket.ServerProtocolControl
    reactor.listenTCP(port, factory)
    reactor.run()


def websocket_data(port, src_queue, rec_queue, det_queue, sample_freq):
    log.startLogging(sys.stdout)
    factory = ss.websocket.ServerProtocolDataFactory(url="ws://localhost:{}".format(port),
                                                     src_queue=src_queue,
                                                     rec_queue=rec_queue,
                                                     det_queue=det_queue,
                                                     sample_freq=sample_freq,
                                                     )
    factory.protocol = ss.websocket.ServerProtocolData
    reactor.listenTCP(port, factory)
    reactor.run()
