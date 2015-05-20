#!/usr/bin/env python
import cogradio_utils as cg
import sys
import matplotlib.pyplot as plt
import Pyro4
from multiprocessing import Process, Queue, Pipe
from twisted.python import log
from twisted.internet import reactor
import argparse
import time


parser = argparse.ArgumentParser(
    description='Cognitive radio compressive sensing process')
parser.add_argument('ip', metavar='ip')
parser.add_argument('f_samp', metavar='f_samp', type=int, default=25e6)
parser.add_argument('N', metavar='N', type=int, default=14)
parser.add_argument('L', metavar='L', type=int, default=40)
args = parser.parse_args()


frequencies = [2e3, 4e3, 5e6, 8e6]
widths = [1000, 1000, 1000, 1000]
ip = args.ip
L = args.L
N = args.N
f_samp = args.f_samp
sample_freq = f_samp
center_freq = 2.41e9

MEERSAMPLESG = 100

nyq_block_size = L * N * MEERSAMPLESG
window_length = nyq_block_size
numbbins = 15
threshold = 2000

# Init blocks
try:
    source = cg.source.UsrpN210(
        addr=ip, samp_freq=f_samp, center_freq=center_freq)
except RuntimeError:
    print "Could not find USRP, falling back to artificial source"
    source = cg.source.Rect(frequencies, widths, f_samp)

sampler = cg.sampling.MultiCoset(N)
C = sampler.generateC()
reconstructor = cg.reconstruction.Wessel(N, L)


def signal_generation(signal, generator, mc_sampler, sample_freq, window_length, opt):
    while True:
        orig_signal = generator.generate(window_length)
        if signal.full():
            signal.get()
        signal.put_nowait(mc_sampler.sample(orig_signal))

        options = None
        while opt.poll():
            options = opt.recv()
        if options:
            print options
            source.parse_options(options)


def signal_reconstruction_profiler(signal, plot_queue, websocket_queue,
                                   reconstructor, opt):

    import cProfile
    import pstats
    import StringIO
    pr = cProfile.Profile()
    pr.enable()
    signal_reconstruction(
        signal, plot_queue, websocket_queue, reconstructor, opt)
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
    pr.dump_stats("Reconstruction_profiling.dmp")


def signal_reconstruction(signal, plot_queue, websocket_queue,
                          reconstructor, opt):
    while True:
        options = None
        set_center_freq = center_freq
        while opt.poll():
            options = opt.recv()
        if options:
            print options
            for key, opt in options.items():
                if key == 'center_freq':
                    set_center_freq = opt * 1e6

        inp = signal.get()
        if inp.any():
            out = cg.fft(reconstructor.reconstruct(inp))
            out_container = cg.websocket.PlotDataContainer(
                sample_freq=sample_freq, center_freq=set_center_freq, data=out)

            if websocket_queue.full():
                websocket_queue.get()
            websocket_queue.put_nowait(out_container)

            if plot_queue.full():
                plot_queue.get()
            plot_queue.put_nowait(out)


def plotter(plot_queue):
    plt.ion()
    while True:
        to_plot = plot_queue.get()
        if to_plot.any():
            plt.cla()
            plt.plot(to_plot)
            plt.draw()
            plt.show()
            plt.pause(0.01)


def websocket(websocket_queue, opt):
    log.startLogging(sys.stdout)
    factory = cg.websocket.WebSocketServerPlotFactory("ws://localhost:9000",
                                                      websocket_queue,
                                                      opt)
    factory.protocol = cg.websocket.ServerProtocolPlot

    reactor.listenTCP(9000, factory)
    reactor.run()


def settings_server(src_opt, rec_opt, web_opt):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    settings = cg.Settings(web_opt, src_opt, rec_opt)
    uri = daemon.register(settings)
    ns.register("cg.settings", uri)
    daemon.requestLoop()


if __name__ == '__main__':
    signal = Queue(10)
    plot_queue = Queue(10)
    websocket_queue = Queue(10)

    parent_opt_src, child_opt_src = Pipe()
    parent_opt_rec, child_opt_rec = Pipe()
    parent_opt_web, child_opt_web = Pipe()

    processes = []
    p1 = Process(target=signal_generation,
                 args=(signal, source, sampler, sample_freq, window_length, child_opt_src))
    p2 = Process(target=signal_reconstruction,
                 args=(signal, plot_queue, websocket_queue,
                       reconstructor, child_opt_rec))
    # p2 = Process(target=signal_reconstruction_profiler,
    #              args=(signal, plot_queue, websocket_queue,
    #                    reconstructor, child_opt_rec))
    p3 = Process(target=settings_server, args=(parent_opt_src, parent_opt_rec,
                                               parent_opt_web))
    p4 = Process(target=websocket, args=(websocket_queue, child_opt_web))

    processes.append(p1)
    processes.append(p2)
    processes.append(p3)
    processes.append(p4)

    try:
        [p.start() for p in processes]
        [p.join() for p in processes]
    except KeyboardInterrupt:
        flag = True
        while flag:
            flag = False
            for p in processes:
                if p.is_alive():
                    flag = True
                    p.terminate()
                    print p, "termination sent"
            time.sleep(1)
    finally:
        sys.exit(1)
