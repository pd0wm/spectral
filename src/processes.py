import cogradio as cg
import cogradio_vis as vis
import Pyro4
import sys
from twisted.python import log
from twisted.internet import reactor
from cogradio_vis.websocket import *


def send_to_websocket(queue, data, dtype):
    container = WebsocketDataContainer(dtype, data)
    container.enqueue(queue)


def run_generator(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor):
    settings = Pyro4.Proxy("PYRONAME:cg.settings")
    while True:
        source.parse_options(settings.read())

        orig_signal = source.generate(block_size)
        sampled = sampler.sample(orig_signal)
        signal_queue.queue(sampled)

        offset = int(block_size / upscale_factor)
        data = cg.fft(cg.auto_correlation(orig_signal, maxlag=offset))
        send_to_websocket(websocket_src_queue, data, ServerProtocolData.SRC_DATA)


def run_reconstructor(signal_queue, websocket_rec_queue, det_queue, reconstructor, sample_freq):
    while True:
        inp = signal_queue.dequeue()
        if inp is not None:
            rx = reconstructor.reconstruct(inp)
            signal = cg.fft(rx)
            det_queue.queue(rx)
            send_to_websocket(websocket_rec_queue, signal, ServerProtocolData.REC_DATA)


def run_detector(detector, detection_queue, websocket_det_queue):
    settings = Pyro4.Proxy("PYRONAME:cg.settings")
    while True:
        detector.parse_options(settings.read())

        inp = detection_queue.dequeue()
        if inp is not None:
            detect = [int(x) for x in detector.detect(inp)]
            send_to_websocket(websocket_det_queue, detect, ServerProtocolData.DET_DATA)


def run_server():
    vis.webserver.flaskr.app.run(host='0.0.0.0', use_reloader=False)


def run_websocket_data(websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq):
    port = 1337
    log.startLogging(sys.stdout)
    factory = ServerProtocolDataFactory(url="ws://localhost:{}".format(port),
                                                      src_queue=websocket_src_queue,
                                                      rec_queue=websocket_rec_queue,
                                                      det_queue=websocket_det_queue,
                                                      sample_freq=sample_freq,
                                                      )
    factory.protocol = ServerProtocolData
    reactor.listenTCP(port, factory)
    reactor.run()


def run_websocket_control():
    port = 1338
    log.startLogging(sys.stdout)
    factory = ServerProtocolControlFactory(url="ws://localhost:{}".format(port))
    factory.protocol = ServerProtocolControl
    reactor.listenTCP(port, factory)
    reactor.run()
