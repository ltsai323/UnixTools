#!/usr/bin/env sh
# usage:
#    ./thisFile.sh remoteFileName localFileName optionName

remotePath=$1
localPath=$2
optionName=$3

echo $1
echo $2
echo $3
echo "/home/ltsai/script/crab/compareTwoFileContent.py -o netpath -rf $remotePath -lf $localPath"
/home/ltsai/script/crab/compareTwoFileContent.py -o netpath -rf $remotePath -lf $localPath
/home/ltsai/script/crab/downloadNCHCFile.sh netpath $optionName update
