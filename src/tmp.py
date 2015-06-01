import cogradio as cg
import numpy as np

signal = np.linspace(0, 99, 100)
sampler = cg.sampling.Coprime(5, 7)
out = sampler.sample(signal)

print out.shape
print out

