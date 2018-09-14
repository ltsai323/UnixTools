#!/usr/bin/env python2
command='"cd /wk_cms/ltsai/LbFrame/MC/lotofRun && cmsRun BPH-RunIISpring16DR80-00058_1_cfg.py runNum={} fileList=fLink{:02d} && cmsRun BPH-RunIISpring16DR80-00058_2_cfg.py runNum={} && /bin/rm BPH-RunIISpring16DR80-00058_step1_{:02d}.root"'
runNumberFrom=20
runNumberTo=30
import os

# use for specificFileName
spNum=[20]
for i in spNum:
#for i in range(runNumberFrom, runNumberTo):
    os.system('./submitJOB.py --command={} --name={}'.format(command.format(i,i,i,i), 'runMCjob_{:02d}'.format(i)))
