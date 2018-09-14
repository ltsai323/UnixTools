#!/usr/bin/env python

### Remark optparse is replaced with argparth in python 2.7.

import sys, os, shutil, re, subprocess, time
from   optparse import OptionParser
# import ROOT

pbsBatchTemplate = """#!/usr/bin/env bash

#PBS -V
#PBS -j oe
#PBS -q cms
#PBS -N JOBNAME
#PBS -d JOBDIR
#PBS -o JOBSTDOUT
#PBS -e JOBSTDERR

#RUNLABEL=1
#if ["${RUNLABEL}" -gt 0 ]; then

if [ ! -e JOBDIR/pbsDone ]; then
cd JOBDIR
CMD
fi

#touch JOBDIR/pbsDone

"""

def main():
    # parse all options
    parser = OptionParser()
    parser.add_option('-t', '--tag' , dest='tag' , help='The tag to mark the batchJob', type='string')
    parser.add_option('-f', '--file', dest='file', help='The filename keeps tasks line-by-line', type='string')
    (opt, args) = parser.parse_args()

    if opt.file is None:
        print "'-f YOUR_TASK_FILE' is mandatory. Abort"
        return 0

    if opt.tag is None:
        workTag = ''
    else:
        workTag='_'+opt.tag
    workDir=os.path.abspath(os.path.join(os.getcwd(),"batchJobs"+workTag))
    if not os.path.exists(workDir):
        os.mkdir(workDir, 0755)
    shutil.copy2('/wk_cms/pchen/commonTools/batch/batchSubmit.py',workDir)

    # Start loop
    f = open(opt.file,"r")
    for jobID, cmd in enumerate(f, start=0):
        jobDir = os.path.join(workDir,"{0:04d}".format(jobID))
        if not os.path.exists(jobDir):
            os.makedirs(jobDir, 0755)
        cmd = cmd.lstrip().rstrip('\n')
        batchScriptFile = open(os.path.join(workDir,"job_{0:04d}.sh".format(jobID)),'w')
        batchScript = re.sub('JOBDIR',jobDir,pbsBatchTemplate)
        batchScript = re.sub('JOBNAME',"{0:04d}{1}".format(jobID,workTag),batchScript)
        batchScript = re.sub('JOBSTDOUT',os.path.join(jobDir,'stdout.log'),batchScript)
        batchScript = re.sub('JOBSTDERR',os.path.join(jobDir,'stderr.log'),batchScript)
        batchScript = re.sub('CMD',cmd,batchScript)
        batchScriptFile.write(batchScript)
        batchScriptFile.close()
    f.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())


