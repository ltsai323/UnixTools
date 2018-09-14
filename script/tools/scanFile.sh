#!/usr/bin/env sh
# search for input word in the file of this directory
# usage:
#        ./thisfile.sh Words fileName

searchContent=$1
searchFiles=$2

i=0

for name in `ls  | grep "$searchFiles"`
    do
        echo ${i}". "${name}
        cat $name | grep "$searchContent"
        echo
        i=$(( $i+1 ))
    done
