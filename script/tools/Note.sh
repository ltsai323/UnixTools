#!/usr/bin/env sh

if [ "$1" == "" ]; then
    echo "you need to input a file"
    exit -1
fi

echo "" >> $1 && date >> $1
vi $1

