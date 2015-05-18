#!/usr/bin/env python
import cogradio_utils as cg
import sys
import matplotlib.pyplot as plt
import Pyro4
from multiprocessing import Process, Queue, Pipe
from twisted.python import log
from twisted.internet import reactor
import numpy as np

frequencies = [2e3, 4e3, 5e6, 8e6]
widths = [1000, 1000, 1000, 1000]
L = 40
N = 14
nyq_block_size = L * N
f_samp = 25e6
window_length = L * N
numbbins = 15
threshold = 2000

# Init blocks
try:
    source = cg.source.UsrpN210(addr="192.168.20.2", samp_freq=f_samp, center_freq=2.41e9)
except RuntimeError:

    #source = cg.source.Rect(frequencies, widths, f_samp)
    source = cg.source.ComplexExponential(frequencies, f_samp)

sampler = cg.sampling.MultiCoset(N)
C = sampler.generateC()
reconstructor = cg.reconstruction.Wessel(N, L)

def signal_generation(signal, generator, mc_sampler, f_samp, window_length, opt):
    while True:
        orig_signal = generator.generate(window_length)
        if signal.full():
            signal.get()
        # signal.put_nowait(orig_signal)
        signal.put_nowait(mc_sampler.sample(orig_signal))


def signal_reconstruction(signal, plot_queue, websocket_queue,
                          reconstructor, opt):
    while True:
        inp = signal.get()
        if inp.any():
            out = cg.fft(reconstructor.reconstruct(inp))
            # out = cg.fft(inp)
            out_container = cg.websocket.PlotDataContainer(f_samp, out)

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
    settings = cg.Settings(web_opt)
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
                 args=(signal, source, sampler, f_samp, window_length, child_opt_src))
    p2 = Process(target=signal_reconstruction,
                 args=(signal, plot_queue, websocket_queue,
                       reconstructor, child_opt_rec))
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
        [p.terminate() for p in processes]
        print "Termination signals sent"
        sys.exit(1)
