import cogradio_utils as cg
import sys
import Pyro4
from multiprocessing import Queue, Pipe
from twisted.python import log
from twisted.internet import reactor


def run_generator(signal_queue, source, sampler, sample_freq, window_length, opt):
    while True:
        orig_signal = source.generate(window_length)
        if signal_queue.full():
            signal_queue.get()
        signal_queue.put_nowait(sampler.sample(orig_signal))

        options = None
        while opt.poll():
            options = opt.recv()
        if options:
            source.parse_options(options)


def run_reconstructor(signal_queue, websocket_queue, reconstructor, sample_freq, center_freq, opt):
    while True:
        inp = signal_queue.get()
        if inp.any():
            signal = cg.fft(reconstructor.reconstruct(inp))

            if websocket_queue.full():
                websocket_queue.get()

            websocket_queue.put_nowait(signal)


def run_reconstructor_profiled(signal_queue, websocket_queue, reconstructor, sample_freq, center_freq, opt):
    import cProfile
    import pstats
    import StringIO
    pr = cProfile.Profile()
    pr.enable()
    run_reconstructor(signal_queue, websocket_queue, reconstructor, sample_freq, center_freq, opt)
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
    pr.dump_stats("Reconstruction_profiling.dmp")


def run_websocket_server(websocket_queue, sample_freq, center_freq, opt):
    log.startLogging(sys.stdout)
    factory = cg.websocket.WebSocketServerPlotFactory(url="ws://localhost:9000", queue=websocket_queue,
                                                      sample_freq=sample_freq, center_freq=center_freq,
                                                      opt=opt)
    factory.protocol = cg.websocket.ServerProtocolPlot

    reactor.listenTCP(9000, factory)
    reactor.run()


def run_settings_server(web_opt, src_opt, rec_opt):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    settings = cg.Settings(web_opt, src_opt, rec_opt)
    uri = daemon.register(settings)
    ns.register("cg.settings", uri)
    daemon.requestLoop()
