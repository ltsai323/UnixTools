#!/usr/bin/env sh
g++ `root-config --libs --cflags ` -lRooFitCore -lRooFit -lMinuit $1 -o a -O3  && time ./a > log_rooFit
#g++ `root-config --libs --cflags ` -lRooFitCore -lRooFit -lMinuit $1 -o a -O3  && ./a 
echo "RooFit output is stored in log_rooFit"
