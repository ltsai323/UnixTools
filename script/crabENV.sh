#!/usr/bin/env sh
source /cvmfs/cms.cern.ch/crab3/crab.sh && echo "crab.sh loaded"
source /cvmfs/cms.cern.ch/crab3/crab_standalone.sh && echo 'crab_standalone.sh loaded'
source /cvmfs/cms.cern.ch/common/crab-setup.sh && echo "crab env of python is ready"

cd $CMSSW_BASE/src
eval `scramv1 runtime -sh` # = cmsenv
cd -


echo "crab envirnment is ready"
