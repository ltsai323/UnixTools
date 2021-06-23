#!/usr/bin/env sh
g++ `root-config --libs --cflags` $1 -o $2 -O3
