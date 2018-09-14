#!/usr/bin/env bash

#PBS -V
#PBS -j oe
#PBS -q cms
#PBS -N 0000
#PBS -d /wk_cms/pyu/HWAnalysis/eleSF/egm_tnp_analysis/batchJobs/0000
#PBS -o /wk_cms/pyu/HWAnalysis/eleSF/egm_tnp_analysis/batchJobs/0000/stdout.log
#PBS -e /wk_cms/pyu/HWAnalysis/eleSF/egm_tnp_analysis/batchJobs/0000/stderr.log

#RUNLABEL=1
#if ["${RUNLABEL}" -gt 0 ]; then

if [ ! -e /wk_cms/pyu/HWAnalysis/eleSF/egm_tnp_analysis/batchJobs/0000/pbsDone ]; then
cd /wk_cms/pyu/HWAnalysis/eleSF/egm_tnp_analysis/
source etc/scripts/setup.sh
python tnpEGM_fitter.py etc/config/settings_ele_page.py --flag passingTight80X --createBins 
python tnpEGM_fitter.py etc/config/settings_ele_page.py --flag passingTight80X --createHists 
python tnpEGM_fitter.py etc/config/settings_ele_page.py --flag passingTight80X --doFit
python tnpEGM_fitter.py etc/config/settings_ele_page.py --flag passingTight80X --doFit --mcSig --altSig
python tnpEGM_fitter.py etc/config/settings_ele_page.py --flag passingTight80X --doFit --altSig
python tnpEGM_fitter.py etc/config/settings_ele_page.py --flag passingTight80X --doFit --altBkg
python tnpEGM_fitter.py etc/config/settings_ele_page.py --flag passingTight80X --sumUp 
fi

#touch /wk_cms/pyu/HWAnalysis/eleSF/egm_tnp_analysis/batchJobs/0000/pbsDone

