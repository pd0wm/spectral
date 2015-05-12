#!/usr/bin/env python
import cogradio_utils as cg
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import Pyro4

frequencies = [0.3421, 0.3962, 0.1743, 0.1250]
L = 50
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
        #if signal.qsize() < 10:
        signal.put(mc_sampler.sample(orig_signal))


def signal_reconstruction(signal, plot_queue, reconstructor):
    while True:
        inp = signal.get()
        if inp.any():
            out = reconstructor.reconstruct(inp)
            # if plot_queue.qsize() < 10:
            plot_queue.put(out)


def plotter(plot_queue):
    print "Mac is voor winnaars"
#    plt.ion()
#    while True:
#        to_plot = plot_queue.get()
#        if to_plot.any():
#            plt.cla()
#            plt.plot(cg.fft(to_plot))
#            plt.draw()
#            plt.show()
#            plt.pause(0.01)


def settings_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    settings = cg.Settings()
    uri = daemon.register(settings)
    ns.register("cg.settings", uri)
    daemon.requestLoop()

if __name__ == '__main__':
    signal = Queue()
    plot_queue = Queue()

    p1 = Process(target=signal_generation,
                 args=(signal, source, sampler, f_samp, window))
    p2 = Process(target=signal_reconstruction,
                 args=(signal, plot_queue, reconstructor))
    p3 = Process(target=plotter, args=(plot_queue,))
    p4 = Process(target=settings_server)


    try:
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
        p3.terminate()
        p4.terminate()

