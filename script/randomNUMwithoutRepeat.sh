#!/usr/bin/env sh



# create a empty file to store random number generated.
# if random number is the same, skip this random number.
echo "" > .randomHistory.txt

num=0


while [ "$num" != "100" ]
do
    NUM=`printf '%03i' ${num}`
    randomNUM=${RANDOM}
    historyCheck=`cat .randomHistory.txt | grep "${randomNUM}"`
    if [ "${historyCheck}" == "" ]; then
        echo ${NUM}
        echo ${randomNUM} >> .randomHistory.txt
    else
        echo ${num}' skipped'
        num=$(( ${num} - 1 ))
    fi
    num=$(( ${num} + 1 ))
done

rm .randomHistory.txt
