#!/usr/bin/env bash

echo '' > log_fitResCollection
for name in `ls store_root/*.root | grep ptRange | grep shortRangeLbFit`;
do
    addInfo='2aTFile* _file0 = TFile::Open("'$name'");'
    echo $name
    echo $name >> log_fitResCollection
    sed -e"$addInfo" template_simpleCheckLbTk.C > tmp.C
    root -b -q tmp.C >> log_fitResCollection
done
mv log_fitResCollection log_fitResCollectionLbTk
rm tmp.C
