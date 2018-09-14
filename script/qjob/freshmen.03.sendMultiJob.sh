#!/usr/bin/env sh

SEED=8000

while [ "$SEED" != "${1}" ]
do
    sed "9arandomSeed=${SEED}" freshmen.01.qsubSample.sh > jobSent.sh
    #bsub -R "pool>10000" -q 8nh  -J No_${SEED} < jobSent.sh
    qsub jobSent.sh -N "JOB_$SEED"
    SEED=$(($SEED + 1 ))
done


rm jobSent.sh
