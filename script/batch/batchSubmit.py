#!/usr/bin/env python

### Remark: optparse is replaced with argparth since py27.
###         subprocess.check_output is available since py27

import sys, os, shutil, re, subprocess, time
from   optparse import OptionParser
# import ROOT

bunchSize  = 100
maxRunJobs = 100
maxQueJobs = 200
submitGap  = 2. # Gap between submissions.


def isQstatOk(queue='cms', limit=100):
    # check number of running jobs instead of on queue.
    s = subprocess.Popen('qstat -q | grep '+queue+' | awk \'{printf("%d,%d",$6,$7)}\'', shell=True, stdout=subprocess.PIPE)
    time.sleep(20)
    sout, serr = s.communicate()
    sout = sout.split(',')
    print sout[0], sout[1]
    if len(sout) == 2 and int(sout[0]) < maxRunJobs and int(sout[1]) < maxQueJobs:
        return True
    print "Queue is full, halt for few seconds..."
    return False

def main():
    # parse all options
    parser = OptionParser()
    parser.add_option('-f', '--format', dest='jobFormat', help='The regex to isolate the batchJob', default='job_.*.sh', type='string')
    (opt, args) = parser.parse_args()

    workDir = os.path.abspath(os.getcwd())
    jobFormat = re.compile(opt.jobFormat)

    # Start loop
    fcounter=0
    for f in os.listdir(workDir):
        if not jobFormat.match(f):
            continue
        jobFile = open(os.path.join(workDir,f))
        for line in jobFile.readlines():
            line = line.rstrip('\n').split()
            if len(line) == 3 and line[0] == '#PBS' and line[1] == '-d':
                jobWorkDir = line[2]
                break
        jobFile.close()
        if os.path.exists(os.path.join(jobWorkDir,'pbsDone')):
            continue;
        if fcounter%bunchSize==0 :
            while(not isQstatOk()):
                time.sleep(3)
        subprocess.Popen('qsub '+os.path.join(workDir,f), shell=True)
        fcounter+=1
        time.sleep(submitGap)

    return 0

if __name__ == "__main__":
    sys.exit(main())

