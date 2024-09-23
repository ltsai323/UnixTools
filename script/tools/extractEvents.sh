#!/usr/bin/env sh

nevt=$1
ifile=$2
tin=$3

ofile=output.root

if [ "$nevt" == "" ]; then
    nevt=1
fi
if [ "$tin" == "" ]; then
    tin=t
fi


echo "extract $nevt event of tree:$tin from $ifile"
sleep 3


root -b <<EOF
auto ifile = TFile::Open("${ifile}");
auto itree = (TTree*) ifile->Get("${tin}");

auto ofile = new TFile("${ofile}", "RECREATE");
ofile->cd();
auto otree = (TTree*) itree->CloneTree(${nevt});
otree->Write();
ofile->Close();
EOF

echo "done. output file is $ofile"
