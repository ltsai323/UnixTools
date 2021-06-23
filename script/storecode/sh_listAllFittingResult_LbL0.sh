#!/usr/bin/env bash

echo '' > log_fitResCollection
for name in `ls store_root/*.root | grep ptRange | grep LbL0Shape`;
do
    addInfo='2aTFile* _file0 = TFile::Open("'$name'");'
    echo $name
    echo $name >>log_fitResCollection
    sed -e"$addInfo" template_simpleCheckLbL0.C > tmp.C
    root -b -q tmp.C >> log_fitResCollection
done
mv log_fitResCollection log_fitResCollectionLbL0
rm tmp.C
