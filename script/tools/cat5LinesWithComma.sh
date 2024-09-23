#!/bin/bash

file=$1
chunk_size=${2:-5}


while IFS= read -r line
do
    args=("$line")
    for ((i=1; i<$chunk_size; i++)); do
        if IFS= read -r line; then
            args+=("$line")
        else
            break
        fi
    done

    IFS=','
    echo "${args[*]}"
done < "$file"

# example code
# for a in `sh thisfile.sh theTEXT.txt 3`; do echo [$a]; done
