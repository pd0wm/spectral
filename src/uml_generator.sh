#!/usr/bin/env bash

INP_DIR="./spectral.core/";
OUT_DIR="../doc/thesis/implementation/model/figures/"
TOP_LEVEL="spectral.core";

DIR_MATCHER="*/"
PIC_TYPE="eps"

files=$(ls -d $INP_DIR$DIR_MATCHER);
for file in $files; do
    echo $file
    IFS='/' read -a path <<< "$file"
    mod=${path[2]}
    echo $OUT_DIR$mod
    pyreverse -o $PIC_TYPE -p $mod $file;
done

pyreverse -o $PIC_TYPE -k -p $TOP_LEVEL $TOP_LEVEL
mv classes* $OUT_DIR
mv packages* $OUT_DIR


