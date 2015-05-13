#!/usr/bin/env python
import cogradio_utils as cg
import sys
import matplotlib.pyplot as plt
import Pyro4
from multiprocessing import Process, Queue, Pipe
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
                                        WebSocketServerProtocol

frequencies = [0.3421, 0.3962, 0.1743, 0.1250]
L = 20
N = 14
nyq_block_size = L * N
f_samp = 1
window = L * N
numbbins = 15
threshold = 2000

# Init blocks
source = cg.source.Sinusoidal(frequencies, SNR=5)
sampler = cg.sampling.MultiCoset(N)
C = sampler.generateC()
reconstructor = cg.reconstruction.CrossCorrelation(N, L, C)

def signal_generation(signal, generator, mc_sampler, f_samp, window, opt):
    while True:
        orig_signal = generator.generate(f_samp, window)
        if signal.full():
            signal.get()
        signal.put_nowait(mc_sampler.sample(orig_signal))


def signal_reconstruction(signal, plot_queue, websocket_queue, reconstructor, opt):
    while True:
        inp = signal.get()
        if inp.any():
            out = cg.fft(reconstructor.reconstruct(inp))
            if websocket_queue.full():
                websocket_queue.get()
            websocket_queue.put_nowait(out)

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
                                                      websocket_queue)
    factory.protocol = cg.websocket.ServerProtocolPlot

    reactor.listenTCP(9000, factory)
    reactor.run()


def settings_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    settings = cg.Settings()
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
                 args=(signal, source, sampler, f_samp, window, child_opt_src))
    p2 = Process(target=signal_reconstruction,
                 args=(signal, plot_queue, websocket_queue, reconstructor, child_opt_rec))
    p3 = Process(target=settings_server, parent_opt_src, parent_opt_rec, parent_opt_web)
    p4 = Process(target=websocket, args=(websocket_queue, child_opt_web))

    processes.append(p1)
    processes.append(p2)
    processes.append(p3)
    processes.append(p4)

    try:
        [p.start() for p in processes]
        while True:
            plotter(plot_queue)
        [p.join() for p in processes]
    except KeyboardInterrupt:
        [p.terminate() for p in processes]
        print "Termination signals send"
        sys.exit(1)
