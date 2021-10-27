#!/usr/bin/env python2


import os
# input arguments :
# 1. input filepath.txt
# 2. input current directory
template_shellScript='''#!/usr/bin/env sh

filenameOnly=`extractfilename.sh $1`
outputDir=$2

mydir=$filenameOnly

if [ "$1" == "" ]; then
    echo "you need to input a text file"
    exit
fi

mkdir -p $outputDir/$mydir
idx=0
for file in `cat $1`;
do
    xrdcp -f $file running.root
    {exeFile} running.root $idx
    let "idx=idx+1"
    mv output*.root $outputDir/$mydir/
done

hadd $outputDir/$mydir.root $outputDir/$mydir/*.root
'''

template_condorScript='''universe = vanilla
Executable = {script}
+JobFlavour={period}
should_transfer_files = NO
use_x509userproxy = true
Output = /home/ltsai/condorlogs/log_job_$(Process)_output
Error  = /home/ltsai/condorlogs/log_job_$(Process)_error
Log    = /home/ltsai/condorlogs/log_job_$(Process)_log
RequestCpus = 1

max_retries = 1
Arguments  = $(filepath) {PWD}
Queue filepath from {pathlist}
'''
def checkexist(file):
    if not os.path.isfile(file):
        raise IOError('input file "%s" does not exist'%file)

workperiod={ 0:'espresso', 1:'longlunch', 2:'workday', 3:'tomorrow', 4:'testmatch', 5:'nextweek'}
def GetFromArg():
    import sys
    if len(sys.argv) == 1: raise ValueError('Input a shell script or one line bash command.')
    if '.sh' in sys.argv[1]: return sys.argv[1]
    tmpfile='/tmp/sendscript.sh'
    f=open(tmpfile, 'w')
    f.write( '#!/usr/bin/env sh\n' )
    f.write( sys.argv[1] )
    f.close()
    return tmpfile

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3: raise ValueError('input args : 1.bashScript, 2.input text list')
    inputscript=GetFromArg()
    mypaths=sys.argv[2]
    checkexist(mypaths)
    checkexist(inputscript)


    condorscript=open('/tmp/condorSubmitScript.SUB', 'w')
    condorscript.write( template_condorScript.format(period=workperiod[3],pathlist=mypaths, script=inputscript, PWD=os.getcwd()) )
    condorscript.close()
    os.system('condor_submit /tmp/condorSubmitScript.SUB')
