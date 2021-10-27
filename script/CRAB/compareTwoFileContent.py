#!/usr/bin/env python2
# useage:
#    ./compareTwoFileContent.py -o netPath -rf remotePath (-lf localPath)

import os
import commands
import argparse
import re

#def simplifyString( pathList ):
#    simplifiedStr=[]
#    for path in pathList:
#        sepStrList=pathList.split('/')
#        rootFileIdx=len(sepStrList)-1
#        simplifiedStr.append(sepStrList[rootFileIdx])
#    return simplifiedStr

def simplifyString( pathList ):
    simplifiedStr=[]
    idx=0
    while idx < len(pathList):
        sepStrList=pathList[idx].split('/')
        rootFileIdx=len(sepStrList)-1
        simplifiedStr.append( (idx, sepStrList[rootFileIdx]) )
        idx+=1
    return simplifiedStr

def compareFileContent( remotePathFileName, localPathFileName ):
    remoteFile=open(remotePathFileName, 'r')
    localFile=open(localPathFileName, 'r')
    lNames=localFile.read().split()
    rNames=remoteFile.read().split()
    _lNames=simplifyString(lNames)
    _rNames=simplifyString(rNames)

    netFileNameList=[]
    for rIdx, rName in _rNames:
        matched=False
        for lIdx, lName in _lNames:
            if rName == lName:
                matched=True
                break
        if matched:
            continue
        # take original name
        netFileNameList.append(rNames[rIdx])

    remoteFile.close()
    localFile.close()

    return netFileNameList

def compareTwoFile( outPathFileName, remotePathFileName, localPathFileName='' ):
    remoteFile=None
    localFile=None

    try:
        remoteFile=open(remotePathFileName, 'r')
    except IOError:
        print "remote path file not found! check your input path!"
        exit()
    withoutCompareLocal=False
    try:
        localFile=open(localPathFileName, 'r')
    except IOError:
        print "local file name doesn't exit, download all of file from remote site."
        withoutCompareLocal=True
    remoteFile.close()

    if withoutCompareLocal:
        os.system( "cp {0} {1}".format(remotePathFileName, outPathFileName) )
        return
    localFile.close()

    netFileNames=compareFileContent( remotePathFileName, localPathFileName )
    newFile=open(outPathFileName, 'w')
    for fName in netFileNames:
        newFile.write( fName+'\n' )
    newFile.close()
    print 'compare complete! output file name is {0}'.format(outPathFileName)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hiiii')
    parser.add_argument(
            '--remoteFile', '-rf', type=str, default='',
            help='input remote path file'
            )
    parser.add_argument(
            '--localFile', '-lf', type=str, default='',
            help='input local path file'
            )
    parser.add_argument(
            '--output', '-o', type=str, default='netPath',
            help='output flie name'
            )
    args=parser.parse_args()
    compareTwoFile( args.output, args.remoteFile, args.localFile )
