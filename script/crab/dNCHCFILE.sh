#!/usr/bin/env sh
#usage: ./thisFile.sh linkFile optionName
# if you want to use optionName exactly, use:
#       ./thisFile.sh linkFile optionName update 

# original command:
#    xrdcp root://se01.grid.nchc.org.tw/???  local/directory/

defaultFolder="${HOME}/Data"
if [ "$1" == "" ]; then
    echo "need to input link file in NCHC"
    exit
fi

# use date to be the folder name
if [ "`date | cut -d" " -f3`" != "" ]; then
    MON=` date | cut -d" " -f2`
    DAY=` date | cut -d" " -f3`
    YEAR=`date | cut -d" " -f6`
else
    MON=` date | cut -d" " -f2`
    DAY=` date | cut -d" " -f4`
    YEAR=`date | cut -d" " -f7`
fi
option='_'$2
folderName=CRABdata_${DAY}_${MON}_${YEAR}${option}
if [ "$3" == "update" ]; then
    folderName=$2
fi

ls $defaultFolder
if [ `echo $?` != 0 ]; then
    echo "you need to modify default folder to store data"
    exit 0
fi
mkdir -p $defaultFolder/CRABdata/$folderName
for name in `cat $1 | grep '.root'`
do
    xrdcp root://se01.grid.nchc.org.tw/${name} $defaultFolder/CRABdata/${folderName}/
done
