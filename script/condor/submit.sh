#!/usr/bin/env sh
remoteFile=$1
processNum=$2
currentPath=$PWD
export X509_USER_PROXY=/afs/cern.ch/user/l/ltsai/.x509up_54608
if [ "$X509_USER_PROXY" != "" ]; then
    voms-proxy-info -all
    voms-proxy-info -all -file $X509_USER_PROXY
fi
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/cern.ch/work/l/ltsai/Work/MC/CMSSW_8_0_14/src && eval `scramv1 runtime -sh`
cd $currentPath
cmsRun LbToPcK_py_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_HLT.py inputFile=${remoteFile}
cmsRun LbToPcK_py_RAW2DIGI_RECO_EI_DQM.py
#mv step3.root ~/step3_${bbb}.root
mv step3.root step3_${processNum}.root
