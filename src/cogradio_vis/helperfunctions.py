import cogradio_vis as vis
import sys
import Pyro4
from twisted.python import log
from twisted.internet import reactor


def get_settings_object():
    return Pyro4.Proxy("PYRONAME:cg.settings")


def send_to_websocket(queue, data, dtype):
    container = vis.websocket.WebsocketDataContainer(dtype, data)
    container.enqueue(queue)


def websocket_control(port):
    log.startLogging(sys.stdout)
    factory = vis.websocket.ServerProtocolControlFactory(url="ws://localhost:{}".format(port))
    factory.protocol = vis.websocket.ServerProtocolControl
    reactor.listenTCP(port, factory)
    reactor.run()


def websocket_data(port, src_queue, rec_queue, det_queue, sample_freq):
    log.startLogging(sys.stdout)
    factory = vis.websocket.ServerProtocolDataFactory(url="ws://localhost:{}".format(port),
                                                      src_queue=src_queue,
                                                      rec_queue=rec_queue,
                                                      det_queue=det_queue,
                                                      sample_freq=sample_freq,
                                                      )
    factory.protocol = vis.websocket.ServerProtocolData
    reactor.listenTCP(port, factory)
    reactor.run()
