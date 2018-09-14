#!/usr/bin/env sh

# automatically gen MC fragment

#fileName:
if [ "${1}" != "" ]; then
    targetPy="${1}"
else
    echo "you need to input a file"
    #targetPy="Configuration/GenProduction/python/LbJpsiKP.py"
fi

#number of event
num=5000




### STEP1: GEN-SIM
echo "1"
cmsDriver.py ${targetPy} --fileout file:step1.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot NominalCollision2015 --step GEN,SIM --magField 38T_PostLS1  --no_exec -n ${num}



#### STEP2: DIGI + PU mixing + HLT
#echo "2"
#cmsDriver.py ${targetPy} --filein file:step1.root --fileout file:step2.root --pileup NoPileUp --mc --eventcontent RAWSIM  --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --conditions MCRUN2_74_V9 --step DIGI,L1,DIGI2RAW,HLT:@frozen25ns --magField 38T_PostLS1  --no_exec -n ${num}
#
#
#### STEP3: RECO (or AOD, --eventcontent AOD)
#echo "3"
#cmsDriver.py ${targetPy} --filein file:step2.root --fileout file:step3.root --mc --eventcontent AODSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --conditions MCRUN2_74_V9 --step RAW2DIGI,L1Reco,RECO --magField 38T_PostLS1  --no_exec -n ${num}
