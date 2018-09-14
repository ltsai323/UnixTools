#!/usr/bin/env sh
g++ `root-config --libs --cflags` $1 -o a -O3 && ./a
