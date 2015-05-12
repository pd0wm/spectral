#!/usr/bin/env python
import cogradio_utils as cg
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import logging


# import matplotlib.pyplot as plt
np.set_printoptions(linewidth=800, edgeitems=20, threshold=100)
logging.basicConfig(level=logging.DEBUG)
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
        signal.put(mc_sampler.sample(orig_signal))


def signal_reconstruction(signal, plot_queue, websocket_queue, reconstructor):
    while True:
        inp = signal.get()
        if inp.any():
            out = reconstructor.reconstruct(inp)
            plot_queue.put(out)
            try:
                websocket_queue.put_nowait(out)
            except:
                pass


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


signal = Queue()
plot_queue = Queue()
websocket_queue = Queue(1)

p1 = Process(target=signal_generation,
             args=(signal, source, sampler, f_samp, window))
p2 = Process(target=signal_reconstruction,
             args=(signal, plot_queue, websocket_queue, reconstructor))
p3 = Process(target=plotter, args=(plot_queue,))
p4 = Process(target=websocket, args=(websocket_queue,))

p1.start()
p2.start()
# p3.start()
p4.start()
p1.join()
p2.join()
# p3.join()
p4.join()

# Compressive sensing
# nyq_signal = source.generate(f_samp, window)
# mc_signal = sampler.sample(nyq_signal)
# rx = reconstructor.reconstruct(mc_signal)
# y_s = cg.fft(rx)
#
# # Axis generation
# rx_len = (rx.shape[0])
# f_axis_recon = np.linspace(-0.5, 0.5, rx_len)
#
# # Detection
# # detector = cg.detection.SPFL()
# # detector.detect(rx)
#
# # Plotting
# # Reconstruction
# plt.figure(1)
# plt.subplot(211)
# plt.plot(f_axis_recon, y_s)
#
# # Original
# plt.subplot(212)
# plt.stem(np.linspace(-0.5, 0.5, nyq_signal.shape[0]), cg.psd(nyq_signal))
# plt.show()
