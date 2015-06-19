import pstats
import glob
import os
import StringIO
from tabulate import tabulate

search_items = ['spectral', 'dist-packages', 'python2.7']


def read_stats(inp, key):
    text_stream = StringIO.StringIO()
    stats = pstats.Stats(inp, stream=text_stream)
    stats.sort_stats(*key)
    stats.print_stats()
    text_stream.seek(0)
    return text_stream


def find_highest_index(lst, item):
    indices = [i for i, x in enumerate(lst) if x == item]
    if indices:
        return max(indices)
    else:
        return None


def clean_filename_entry(entry):
    entry = entry.split("/")
    for search in search_items:
        index = find_highest_index(entry, search)
        if index is not None:
            entry = entry[index:]
    return "/".join(entry)


def get_content_from_file(prof_rep):
    for line in prof_rep:
        if "ncalls" in line:
            header = line.strip(' \t\n\r').split()
            break
    data = []
    for line in prof_rep:
        if line == "\n":
            break
        row = line.strip(' \t\n\r').split()
        row[-1] = clean_filename_entry(row[-1])
        data.append(row)

    return {'header': header, 'data': data}


def table_to_file(table, filename):
    build_table = tabulate(content['data'], headers=content['header'], tablefmt="latex_booktabs")
    with open(filename, 'w') as f:
        f.write(build_table)

OUTPUT_DIR = "../doc/thesis/appendix/profiler_reports/"
APPENDIX_NAME = "profiler_reports.tex"
INPUT_DIR = "./profiler_reports/"
OUTPUT_EXT = ".tex"
key = ('cumtime', 'tottime')


if __name__ == "__main__":
    inp_files = [os.path.splitext(os.path.basename(b)) for b in glob.glob(INPUT_DIR + "*")]
    for filetupl in inp_files:
        if filetupl[1] == ".prof":
            input_file = filetupl[0] + filetupl[1]
            output_file = filetupl[0] + OUTPUT_EXT
            raw_report = read_stats(INPUT_DIR + input_file, key)
            content = get_content_from_file(raw_report)
            table_to_file(content, OUTPUT_DIR + output_file)

    lines = ["\\input{{{}}}\n".format(f[0]) for f in inp_files]
    with open(OUTPUT_DIR + APPENDIX_NAME, 'w') as f:
        f.writelines(lines)
