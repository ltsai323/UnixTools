#!/usr/bin/env sh

mylist=$1
mymch=$2
mypid=$3
myname=$4
processID=$5
pathName=`echo $mylist | cut -f1 -d.`

myD=$PWD
export X509_USER_PROXY=/afs/cern.ch/user/l/ltsai/.x509up_54608
if [ "$X509_USER_PROXY" != "" ]; then
    voms-proxy-info -all -file $X509_USER_PROXY
fi
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/cern.ch/work/l/ltsai/Work/PentaResearch/CMSSW_9_4_14_UL/src && cmsenv && eval `scramv1 runtime -sh` && cd $myD
ls
echo "condor job$pathName$processID : start cmsRun" >> ~/logCondor
./VCCAnalyzer.py inputFiles=$mylist mcChannel=$mymch targetPID=$mypid
echo "condor job$pathName$processID : end   cmsRun and transfering" >> ~/logCondor
scp tree_VCCAnalyzer_forTest.root ntu:~/Data/condor/$myname/tree_VCCAnalyzer_${pathName}.root
echo "condor job$pathName$processID :                  transfered     " >> ~/logCondor
