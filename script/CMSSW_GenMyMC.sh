#!/usr/bin/env bash
# vim: set sw=4 sts=4 fdm=marker ft=sh et:

################
# Instructions #
################

# 1. Copy GEN-Fragment.py from git - https://github.com/cms-sw/genproductions/tree/master/python
#                                  - https://github.com/cms-sw/cmssw/tree/CMSSW_7_5_X/Configuration/Generator/python
#                       search /Configuration/GenProductions/python
#                           or /Configuration/Generator/python
#    Remark that Configuration directory must in $CMSSW_BASE/src or found no valid config.
# 2. If not in repository, copy name.dec in GeneratorInterface/ExternalDecays/data/
# 3. scram b (You MUST do this or error occurs in introducing configs.)
# 4. ./GenMyMC.sh


##########################
# Official configuration #
##########################
### Full steps: GEN,SIM,DIGI,L1,DIGI2RAW,HLT,RAW2DIGI,RECO
### Currently use McM ( https://cms-pdmv.cern.ch/mcm/chained_campaigns?page=-1&shown=15 ) to handle all official chains
### Configs of each campaign in a chain should be followed carefully.

### About cmsDriver.py
# Ref: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCmsDriver

if [ "$1" != "" ]; then
    targetPy="$1"
else 
    targetPy="PYTHIA8_Lb2pmnu_NoFilter_CUEP8M1_13TeV_cff.py "
fi

# Search Frontier condition from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
#    Notice that different tags can be applied between GENSIM step and the rest ones..
#genGlobalTag="auto::run2_mc"
#globalTag="auto:run2_mc"
genGlobalTag="auto:mc"
#globalTag="auto:mc"
globalTag="MCRUN2_71_V1::All"
# Search HLTrigger/Configuration/python for all tags
hltTable="HLT"
#hltTable="HLT:GRun"
#hltTable="HLT:7E33v2"

# Search Configuration/StandardSequences/python/mixing.py for all tags.
# Also consult McM for correct PU dataset
puScenario="NoPileUp" #2012_Summer_50ns_PoissonOOTPU, NoPileUp
#puScenario="2012_Summer_50ns_PoissonOOTPU --pileup_input YOUR_PILEUP_SOURCE" # file1.root,file2.root,...
#puScenario="2012_Summer_50ns_PoissonOOTPU --pileup_input das:YOUR_PILEUP_DATASET"

# Others
# '--customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1' could be needed since 74x
# '--customise Configuration/DataProcessing/RecoTLR' could be needed for Run2 dataset processing.

numEvents=500

echo -e "targetPy=\x1B[31m${targetPy}\x1B[0m"
echo -e "nEvents =\x1B[31m${numEvents}\x1B[0m"
echo -e "Tag     =\x1B[31m${globalTag}\x1B[0m"

### STEP0: GEN for acceptance measurement
cmsDriver.py Configuration/GenProduction/python/${targetPy} --step GEN --beamspot Realistic50ns13TeVCollision --conditions ${globalTag} --pileup NoPileUp --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN --no_exec -n ${numEvents}

### STEP1: GEN-SIM
echo -e "\x1B[31mFor local generation, change random number seed by\n\tprocess.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(MYRANDOMSEEDFLAG)\x1B[0m"
#cmsDriver.py Configuration/GenProduction/python/${targetPy} --step GEN,SIM --fileout :ile:step1.root --beamspot Realistic50ns13TeVCollision --conditions ${globalTag} --pileup NoPileUp --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM --no_exec -n ${numEvents}

cmsDriver.py Configuration/GenProduction/python/${targetPy} --fileout step1.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions ${globalTag} --pileup NoPileUp --datamix NODATAMIXER --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1  --no_exec -n ${numEvents} 
#--python_filename ${targetPy}_GEN_SIM.py

### STEP2: DIGI + PU mixing + HLT
echo -e "\x1B[31mDon't forget to add mixPoolSource to \n\tprocess.mix.input.fileNames = cms.untracked.vstring('f1.root','f2.root',)\nUsually RelValProdMinBias dataset is taken as sources. Or you could check by 'runTheMatrix.py --what pileup -ne > runTheMatrix.log'.\x1B[0m"
cmsDriver.py Configuration/GenProduction/python/${targetPy} --step DIGI,L1,DIGI2RAW,${hltTable} --filein file:step1.root --fileout step2.root --conditions ${globalTag} --pileup ${puScenario} --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM-RAW  --filein=$(echo $targetPy | awk -F '/' '{printf("%s",$NF)}' | awk -F '.' 'BEGIN{printf("file:")}NR!=NF{printf("%s",$1)}END{printf("_py_GEN_SIM.root")}') --no_exec -n ${numEvents}

### STEP3: RECO (or AOD, --eventcontent AOD)
#cmsDriver.py Configuration/GenProduction/python/${targetPy} --step RAW2DIGI,L1Reco,RECO --filein file:step2.root --fileout step3.root --conditions ${globalTag} --datamix NODATAMIXER --eventcontent RECOSIM --datatier GEN-SIM-RECO --filein=$(echo $targetPy | awk -F '/' '{printf("%s",$NF)}' | awk -F '.' 'BEGIN{printf("file:")}NR!=NF{printf("%s",$1)}END{printf("_py_DIGI_L1_DIGI2RAW_HLT.root")}') --no_exec -n ${numEvents}
