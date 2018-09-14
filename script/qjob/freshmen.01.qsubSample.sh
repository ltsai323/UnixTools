#!/usr/bin/env sh

#PBS -V
#PBS -j oe
#PBS -q cms
#PBS -d /wk_cms/ltsai/LbFrame/TEST/MCgenerate/CMSSW_7_1_21_patch2/src/workspace/qSubResult/
#PBS -o /wk_cms/ltsai/LbFrame/TEST/MCgenerate/CMSSW_7_1_21_patch2/src/workspace/qSubMessage/
#PBS -e /wk_cms/ltsai/LbFrame/TEST/MCgenerate/CMSSW_7_1_21_patch2/src/workspace/qSubMessage/


cd /wk_cms/ltsai/LbFrame/TEST/MCgenerate/CMSSW_7_1_21_patch2/src && eval `scramv1 runtime -sh`
cmsRun LambdaBToJPsiPK_py_GEN_SIM.py  seed=$randomSeed

