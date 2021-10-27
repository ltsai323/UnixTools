#!/usr/bin/env python
# this pyhon file mainly execute the command many times:
#    xrdfs se01.grid.nchc.org.tw ls /cms/store/user/ltsai/???
# to get crab data
SITE='se01.grid.nchc.org.tw'
USER='ltsai'
myPATH="/cms/store/user/ltsai/crabtest/BsToJpsiPhiV2_BFilter_TuneCUEP8M1_13TeV-pythia8-evtgen/CRAB3__LBSPECIFICDECAY_AODSIM/170727_124209/"


import commands
import re
import os
import argparse

# check the input string is a root file
def isRoot( myName ):
    pattern=re.compile(r'\.root\Z')
    match=pattern.search(myName)
    return match
# check the input string is a log file
def isTar( myName ):
    pattern=re.compile(r'\.tar\.gz\Z')
    match=pattern.search(myName)
    return match
# recursive function to browse remote site to search for files to delete
# if you want to record the path you are searching, put pathHistory.
# return the array with log and root file.
def searchingRemote( inPath, pathHistory=[] ):
    outList=[]
    if isRoot(inPath):
        outList.append(inPath)
    elif isTar(inPath):
        outList.append(inPath)
    else:
        res = commands.getstatusoutput( 'xrdfs {0} ls {1}'.format(SITE,inPath) )
        if res[0] == 0:
            pathHistory.append(inPath)
            if res[1] != '':
                for name in res[1].split():
                    outList.extend(searchingRemote(name,pathHistory))
    return outList

# add parser to the code
def addOption():
    parser = argparse.ArgumentParser(description='This is the code to execute "rm -r myDir" to remote site')
    parser.add_argument(
            '--input', '-i', type=str, default='',
            help='input a initial path to be read in the server'
            )
    parser.add_argument(
            '--site', '-s', type=str, default=SITE,
            help='decide where you want to get data'
            )
    parser.add_argument(
            '--user', '-u', type=str, default=USER,
            help='decide the user folder'
            )
    return parser.parse_args()

if __name__ == "__main__":
    args=addOption()
    SITE=args.site
    USER=args.user
    if args.input == '':
        print 'initial path is not set! please use [--help] or [-h] options to see the manual'
        exit()



    pathHistory=[]
    fileList=searchingRemote(args.input,pathHistory)

    deleteLog=open('./log_rmNCHC.deletedHistory', 'w+') # new line, if file exists, overwrite it.
    for file in fileList:
        os.system( 'xrdfs {0} rm {1}'.format(args.site, file) )
        deleteLog.write( file+'\n' )
    print 'files deleted'

    for path in reversed( pathHistory ):
        os.system( 'xrdfs {0} rmdir {1}'.format(args.site, path) )
        deleteLog.write( path+'\n' )
    print 'paths deleted'

    deleteLog.close()
