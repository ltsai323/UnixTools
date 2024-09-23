#!/usr/bin/env sh
ipath=$1

if [ "$1" == "" ]; then
    echo "NCHC path needed. Abort"
    exit
fi
#xrdcp -r --nopbar root://se01.grid.nchc.org.tw/$ipath .
xrdcp -r  --parallel 4 root://se01.grid.nchc.org.tw/$ipath .
