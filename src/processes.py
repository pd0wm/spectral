import cogradio as cg
import sys
import Pyro4
from cogradio.websocket import ServerProtocolPlot, WebsocketDataContainer
from multiprocessing import Queue, Pipe
from twisted.python import log
from twisted.internet import reactor
import numpy as np


def safe_dequeue(queue):
    if not queue.empty():
        options = queue.get_nowait()
        return options

    return None


def safe_queue(queue, signal):
    if queue.full():
        queue.get()
    queue.put_nowait(signal)


def send_to_websocket(queue, data, dtype):
    container = WebsocketDataContainer(dtype, data)
    container.enqueue(queue)


def run_generator(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor):
    settings = Pyro4.Proxy("PYRONAME:cg.settings")
    while True:
        orig_signal = source.generate(block_size)
        sampled = sampler.sample(orig_signal)
        safe_queue(signal_queue, sampled)

        offset = int(block_size / upscale_factor)
        data = cg.fft(cg.auto_correlation(orig_signal, maxlag=offset))
        send_to_websocket(websocket_src_queue, data, ServerProtocolPlot.SRC_DATA)

        source.parse_options(settings.read())


def run_reconstructor(signal_queue, websocket_rec_queue, det_queue, reconstructor, sample_freq, center_freq):
    while True:
        inp = signal_queue.get()
        if inp.any():
            rx = reconstructor.reconstruct(inp)
            signal = cg.fft(rx)

            safe_queue(det_queue, rx)
            send_to_websocket(websocket_rec_queue, signal, ServerProtocolPlot.REC_DATA)


def run_detector(detector, detection_queue, websocket_det_queue):
    settings = Pyro4.Proxy("PYRONAME:cg.settings")
    while True:
        inp = detection_queue.get()
        if inp.any():
            detect = [int(x) for x in detector.detect(inp)]
            send_to_websocket(websocket_det_queue, detect, ServerProtocolPlot.DET_DATA)

        detector.parse_options(settings.read())

def run_websocket_server(websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq, center_freq):
    settings = Pyro4.Proxy("PYRONAME:cg.settings")
    log.startLogging(sys.stdout)
    factory = cg.websocket.WebSocketServerPlotFactory(url="ws://localhost:9000",
                                                      src_queue=websocket_src_queue,
                                                      rec_queue=websocket_rec_queue,
                                                      det_queue=websocket_det_queue,
                                                      sample_freq=sample_freq,
                                                      center_freq=center_freq,
                                                      )
    factory.protocol = cg.websocket.ServerProtocolPlot

    reactor.listenTCP(9000, factory)
    reactor.run()
