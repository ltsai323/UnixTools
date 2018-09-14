#i/usr/bin/env sh

# copy file to a lot of files, named in 2 digi numbers.
# add some content in the copied files.

# if you want to change to 3 or 4 digi, you need to change the value of $NUM

totnum=20


CopyFileWithNUM()
{
    inputFileName=`echo $1 | cut -d"." -f1`
    inputFileType=`echo $1 | cut -d"." -f2`


    # assign stored directory
    if [ "$2" == "" ]; then
        storeDirectory="copied/"
    else
        storeDirectory=$2

    fi
    
    # create a empty file to store random number generated.
    # if random number is the same, skip this random number.
    echo "" > .randomHistory.txt
    num=0
    while [ "${num}" != "${totnum}" ]
    do
        # add 0 to number, eg: 00, 01, 02
        NUM=`printf '%04i' ${num}`
        randomNUM=${RANDOM}
        historyCheck=`cat .randomHistory.txt | grep "${randomNUM}"`
        
        if [ "${historyCheck}" == "" ]; then
            newName=${inputFileName}"_${NUM}."${inputFileType}

            cp $1 ${storeDirectory}${newName}
            sed -i "8a _Seed=${randomNUM}" ${storeDirectory}${newName}
            sed -i "56 s:step1\.root:step1\/step1\_${NUM}\.root:g" ${storeDirectory}${newName}
            # add random seed process in the file
            sed -i "26a process.RandomNumberGeneratorService.generator.initialSeed = _Seed" ${storeDirectory}${newName}
        else
            # if $RANDOM repeats, throw the dice again.
            num=$(( ${num} - 1 ))
        fi
        num=$(( ${num} + 1 ))
    done


    rm .randomHistory.txt
}



# main function
if [ "$1" == "" ]; then
    echo "you need to input a file at least, optionally you can input a directory secquently"
else
    if [ "$2" == "" ]; then
        CopyFileWithNUM $1 
    else
        CopyFileWithNUM $1 $2
    fi
fi
