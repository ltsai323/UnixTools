#!/usr/bin/env sh




~/script/tools/renewVO.sh
source /cvmfs/cms.cern.ch/crab3/crab_standalone.sh
crab checkwrite --site='T2_TW_NCHC'

# equal to cmsenv
cd $CMSSW_BASE/src
eval `scramv1 runtime -sh`
cd -
