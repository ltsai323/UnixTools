#!/usr/bin/env sh

NCHCpath=$1
if [ "$1" == "" ]; then
    echo 'you need a NCHC path'
    exit
fi

uberftp se01.grid.nchc.org.tw "ls -r /dpm/grid.nchc.org.tw/home$NCHCpath" | awk '/root/ {print $6}' | sed 's;/dpm/grid.nchc.org.tw/home;root://se01.grid.nchc.org.tw/;g'
