#!/usr/bin/env sh
# used for check edm files is readable or not.
# usage:
#    ./thisfile.sh dir/

echo "files in this directory : $1"

mkdir -p ~/Data/brokeFile

cd $1
for file in `ls`
do
    echo "process $file"
    edmDumpEventContent ${file} > .log 2>&1
    if [ "$?" != 0 ]; then
        mv ${file} ~/Data/brokeFile/
    fi
done

echo "the broke file stored in ~/Data/brokeFile"
ls ~/Data/brokeFile/
rm .log
cd -
