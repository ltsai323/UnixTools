#!/usr/bin/env sh
# record the date in Update.txt
# if you input a filename, the script will create the backup file with date.

if [ "`date | cut -d" " -f3`" != "" ]; then
    MON=`date | cut -d" " -f2`
    DAY=`date | cut -d" " -f3`
    YEAR=`date | cut -d" " -f6`
else
    MON=`date | cut -d" " -f2`
    DAY=`date | cut -d" " -f4`
    YEAR=`date | cut -d" " -f7`
fi

#echo "mon =  $MON"
#echo "day =  $DAY"
#echo "year=  $YEAR"

mkdir -p ${HOME}/Work/history
path=${HOME}/Work/history


if [ "${1}" == "" ]; then
    echo "" >> ${path}/Update.txt && echo "At ${PWD}: " >> ${path}/Update.txt && date >> ${path}/Update.txt && echo "modified:" >> ${path}/Update.txt
    vim  ${path}/Update.txt
else
    mkdir -p history
    NEWFILENAME="${1}_${MON}_${DAY}_${YEAR}"
    cp $1 history/$NEWFILENAME
    cp $1 ~/Work/history/fileHistory/$NEWFILENAME
    echo "" >> ${path}/Update.txt && echo "At ${PWD}: " >> ${path}/Update.txt && date >> ${path}/Update.txt && echo "modified:" >> ${path}/Update.txt && echo "    ${NEWFILENAME} created!" >> ${path}/Update.txt
    vim  ${path}/Update.txt
fi
