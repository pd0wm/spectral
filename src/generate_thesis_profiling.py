import pstats
import glob
import os


def sort_and_write_stats(inp, out, key):
    with open(out, 'w') as out:
        stats = pstats.Stats(inp, stream=out)
        stats.sort_stats(*key)
        stats.print_stats(5)

OUTPUT_DIR = "../doc/thesis/performance/profiling_reports/"
INPUT_DIR = "./profiler_reports/"
OUTPUT_EXT = ".txt"
key = ('cumtime', 'tottime')

inp_files = [os.path.splitext(os.path.basename(b)) for b in glob.glob(INPUT_DIR + "*")]
for inp in inp_files:
    if inp[1] == ".prof":
        sort_and_write_stats(INPUT_DIR + inp[0] + inp[1], OUTPUT_DIR + inp[0] + OUTPUT_EXT, key)
