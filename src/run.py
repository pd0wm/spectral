#!/usr/bin/env python
import cogradio_utils as cg
import matplotlib.pyplot as plt
import Pyro4
from multiprocessing import Process, Queue

frequencies = [0.3421, 0.3962, 0.1743, 0.1250]
L = 10
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


def signal_generation(signal, generator, mc_sampler, f_samp, window):
    while True:
        orig_signal = generator.generate(f_samp, window)
        if signal.full():
            signal.get()
        signal.put_nowait(mc_sampler.sample(orig_signal))


def signal_reconstruction(signal, plot_queue, websocket_queue, reconstructor):
    while True:
        inp = signal.get()
        if inp.any():
            out = reconstructor.reconstruct(inp)
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
            plt.plot(cg.fft(to_plot))
            plt.draw()
            plt.show()
            plt.pause(0.01)


def websocket(websocket_queue):
    import sys

    from twisted.python import log
    from twisted.internet import reactor
    from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

    log.startLogging(sys.stdout)

    factory = cg.websocket.WebSocketServerPlotFactory("ws://localhost:9000", websocket_queue)
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
    websocket_queue = Queue(1)
    processes = []

    p1 = Process(target=signal_generation,
                 args=(signal, source, sampler, f_samp, window))
    p2 = Process(target=signal_reconstruction,
                 args=(signal, plot_queue, websocket_queue, reconstructor))
    p3 = Process(target=plotter, args=(plot_queue,))
    p4 = Process(target=settings_server)
    p5 = Process(target=websocket, args=(websocket_queue,))

    processes.append(p1)
    processes.append(p2)
    processes.append(p3)
    processes.append(p4)
    processes.append(p5)

    try:
        [p.start() for p in processes]
        [p.join() for p in processes]
    except KeyboardInterrupt:
        [p.terminate for p in processes]
