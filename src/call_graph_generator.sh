INPUT_DIR="profiler_reports/"
OUTPUT_DIR="../doc/thesis/appendix/profiler_reports/"
FORMAT="eps"
extension=".eps"

files=$(ls $INPUT_DIR);
for file in $files; do
    IFS='.' read -a split <<< "$file"
    name=${split[0]}
    echo $name
    gprof2dot -f pstats -c print $INPUT_DIR$file | dot -T$FORMAT > $OUTPUT_DIR$name$extension
done
