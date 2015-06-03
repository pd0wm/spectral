import cogradio as cg
import sys
import Pyro4
import Pyro4.util
from cogradio.websocket import ServerProtocolPlot, WebsocketDataContainer
from multiprocessing import Queue, Pipe
from twisted.python import log
from twisted.internet import reactor
import numpy as np


def run_generator(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor, opt):
    while True:
        orig_signal = source.generate(block_size)
        sampled = sampler.sample(orig_signal)

        if signal_queue.full():
            signal_queue.get()
        signal_queue.put_nowait(sampled)
        act_length = len(orig_signal)
        offset = int(block_size / upscale_factor)
        if len(orig_signal) == block_size:
            container = WebsocketDataContainer(ServerProtocolPlot.SRC_DATA, cg.fft(orig_signal[act_length - offset:act_length + offset]))
            container.enqueue(websocket_src_queue)

        options = None
        while opt.poll():
            options = opt.recv()
        if options:
            source.parse_options(options)


def run_reconstructor(signal_queue, websocket_rec_queue, det_queue, reconstructor, sample_freq, center_freq, opt):
    while True:
        inp = signal_queue.get()
        if inp.any():
            rx = reconstructor.reconstruct(inp)
            signal = cg.fft(rx)

            if det_queue.full():
                det_queue.get()
            det_queue.put_nowait(rx)

            container = WebsocketDataContainer(ServerProtocolPlot.REC_DATA, signal)
            container.enqueue(websocket_rec_queue)


def run_generator_profiler(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor, opt):
    import cProfile
    import pstats
    import StringIO
    pr = cProfile.Profile()
    pr.enable()
    run_generator(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor, opt)
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
    pr.dump_stats("Reconstruction_profiling.dmp")


def run_detector(detector, detection_queue, websocket_det_queue, opt):
    while True:
        inp = detection_queue.get()
        if inp.any():
            detect = [int(x) for x in detector.detect(inp)]
            container = WebsocketDataContainer(ServerProtocolPlot.DET_DATA, detect)
            container.enqueue(websocket_det_queue)

        options = None
        while opt.poll():
            options = opt.recv()
        if options:
            detector.parse_options(options)


def run_websocket_server(websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq, center_freq, opt):
    log.startLogging(sys.stdout)
    factory = cg.websocket.WebSocketServerPlotFactory(url="ws://localhost:9000",
                                                      src_queue=websocket_src_queue,
                                                      rec_queue=websocket_rec_queue,
                                                      det_queue=websocket_det_queue,
                                                      sample_freq=sample_freq,
                                                      center_freq=center_freq,
                                                      opt=opt)
    factory.protocol = cg.websocket.ServerProtocolPlot

    reactor.listenTCP(9000, factory)
    reactor.run()


def run_settings_server(web_opt, src_opt, rec_opt, det_opt):
    try:
        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        settings = cg.Settings(web_opt, src_opt, rec_opt, det_opt)
        uri = daemon.register(settings)
        ns.register("cg.settings", uri)
        daemon.requestLoop()
    except Exception:
        print("Pyro traceback:")
        print("".join(Pyro4.util.getPyroTraceback()))
    finally:
        daemon.close()
