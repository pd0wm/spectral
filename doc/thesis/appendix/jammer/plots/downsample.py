import numpy as np

files = ['system.txt', 'gain.txt', 'phase.txt']

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

for path in files:
    f = open(path)
    next(f)                         # Skip header line
    next(f)

    N = 1000

    d = {}
    for line in f:
        sample = map(float, line.rstrip().replace(' ', '').split('\t'))
        d[sample[0]] = sample[1]

    #start = np.log10(min(d.keys()))
    #stop = np.log10(max(d.keys()))
    start = min(d.keys())
    stop = max(d.keys())

    step = min(d.keys())

    f.close()

    r = open(path.replace('.txt', '_out.txt'), 'w')
    r.write('Freq,Value\n')

    for freq in np.linspace(start, stop, num=N):
        f = find_nearest(d.keys(), freq)

        if f in d:
            print freq, f, step
            r.write(str(f))
            r.write(',')
            r.write(str(d[f]))
            r.write('\n')

    r.close()
