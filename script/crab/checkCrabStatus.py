#!/usr/bin/env python2
# usage: ./thisFile.py
#    edit checkList and execute it, 'dir' can be relative or absolute path

outfilename='log_crabStatus.txt'
checkList=[
{'id': 0,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt100To250_13TeV-amcatnlo-pythia8_v3-ext1-v2_sub01'},
{'id': 1,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt100To250_13TeV-amcatnlo-pythia8_v3-ext2-v2_sub01'},
{'id': 2,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt100To250_13TeV-amcatnlo-pythia8_v3-v3-v2_sub01'},
{'id': 3,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt250To400_13TeV-amcatnlo-pythia8_v3-ext1-v2_sub01'},
{'id': 4,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt250To400_13TeV-amcatnlo-pythia8_v3-ext2-v1_sub01'},
{'id': 5,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt250To400_13TeV-amcatnlo-pythia8_v3-v2_sub01'},
{'id': 6,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt400To650_13TeV-amcatnlo-pythia8_v3-ext1-v2_sub01'},
{'id': 7,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt400To650_13TeV-amcatnlo-pythia8_v3-v2_sub01'},
{'id': 8,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt50To100_13TeV-amcatnlo-pythia8_v3-ext1-v1_sub01'},
{'id': 9,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt50To100_13TeV-amcatnlo-pythia8_v3-v2_sub01'},
{'id':10,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt650ToInf_13TeV-amcatnlo-pythia8_v3-ext1-v2_sub01'},
{'id':11,'dir':'CRAB_projects_ntuples/crab_sigMC_Pt650ToInf_13TeV-amcatnlo-pythia8_v3-v2_sub01'},
]

import sys
import CRABClient
from CRABAPI.RawCommand import crabCommand

logfile=open(outfilename,'w')

for crabInfo in checkList:
    screenSTDout=sys.stdout
    sys.stdout=logfile # redirect the screen output to file
    crabstat=crabCommand('status', dir=crabInfo['dir'])
    sys.stdout=screenSTDout # return the screen output

    print 'Job {idx}:{name} reports the status : {stat}'.format(idx=crabInfo['id'],name=crabInfo['dir'],stat=crabstat['jobsPerStatus'] )
    if 'failed' in crabstat['jobsPerStatus']:
        crabCommand('resubmit', dir=crabInfo['dir'])
        print ' -- the Job has been resubmitted'
    else:
        print ' -- no failed job found, nothing to do.'


logfile.close()
