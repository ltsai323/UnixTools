#!/usr/bin/env sh

inputFile=$1

if [ "$(cat $inputFile | grep '\\n')" == "" ]; then
    sed -i '1,$s:$:\\n:g' $inputFile
fi
