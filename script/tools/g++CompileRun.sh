#!/usr/bin/env sh
# used for g++ compile and automaticlly run.
# the output file is .a

if [ "$1" == "" ]; then
    echo "you need to input a c++ file to be run"
else
    g++ -std=c++0x $1 -o .a && ./.a
fi
