#!/usr/bin/env python2
# default only one command to be executed.
# if you want to do more than one, modify this file
# usage:
#    ./separateFileList.py -i myFileList.txt -n 20 -d /tmp/ltsai/tmpFileList/
#    and myFileList.txt should owns the content:
#        /home/ltsai/Data/bjob/MC_LbTk_180430/LbToJPsiPK_GENSIM_pythia8.00969.root
#        /home/ltsai/Data/bjob/MC_LbTk_180430/LbToJPsiPK_GENSIM_pythia8.01147.root
#        and so on
# usage2:
#    ./separateFileList.py -f data_RunH -n 20 -d /tmp/ltsai/tmpFileList/
#    where dataRunH means the file:
#        $CMSSW_BASE/src/histProduce/histProduce/python/data_RunH_cfi.py
defaultStorageFolder='/tmp/{}/tmpFileList/'
USER='ltsai'



#############################################################
# create file lists to load by tCreate
# usage: 
#  1. put dirList: [ '/a/b/1.root', '/a/b/2.root', ... ]
#  2. put outFileName: result01. it will output result01.root
#  3. put outFolder: /a/b/c/. if not set, use default value
#############################################################
def fileListCreat( fileDirList, storageFileName, storageFolder=defaultStorageFolder ):
    import commands
    import re
    if not fileDirList:
        print 'Error, there is nothing in filelist!'
        exit()

    check=commands.getstatusoutput( 'ls {0}'.format(storageFolder) )
    if check[0]:
        print 'Error, tmp folder to store filelist is not created! please check'
        print 'storage folder:{}'.format(storageFolder)
        print 'code: {}'.format(check[0])
        exit()

    fileListTemplate='''
import FWCore.ParameterSet.Config as cms

files = cms.vstring()
files.extend( [
{0}
 ] )

process = cms.PSet()

process.runSetting = cms.PSet(
        maxEvents = cms.int32(-1),
        outEvery  = cms.uint32(0),
        outName   = cms.string('{1}.root'),
        )
process.inputFiles = cms.PSet( fileNames  = files )
'''
    dirs=''
    mode = re.match(r'"/\w+', fileDirList[0])
    if mode:
        print 'hii'
        dirs='\n'.join(fileDirList)
    else:
        formatted_list=[ '"{}"'.format(item) for item in fileDirList ]
        dirs=',\n'.join(formatted_list)
    outFile=open('{}{}_cfi.py'.format(storageFolder, storageFileName), 'w' )
    outFile.write( fileListTemplate.format(dirs, storageFileName) )
    outFile.close()
    print 'output file: {}{}_cfi.py'.format(storageFolder, storageFileName)
    return

################################
# extract root files from a file
################################
def getRootFiles( fName, num ):
    import re

    myFile=open( fName, "r" )

    oneline=myFile.readline()

    rootList=[]
    while oneline:
        fName=oneline.splitlines()[0]
        mode = re.search( r'\w+\.root",$', fName )
        mode2= re.search( r'\w+\.root$'  , fName )
        if mode:
            rootList.append( fName )
        elif mode2:
            rootList.append( fName )

        oneline=myFile.readline()
    myFile.close()
    return getSepLists( rootList, num )


################################
# separate files into N location
################################
def getSepLists( fNameList, num ):
    fList=[ [] for i in range(num) ]
    i=0
    idx=0
    Size=len(fNameList)
    for idx in range(Size):
        fList[i].append(fNameList[idx])
        i+=1
        if i == num:
            i=0
    outList=[]
    for i in range(num):
        outList.append(fList[i])
    return outList

######################
# get CMSSW envirnment
######################
def getCMSSWVersion():
    import commands
    baseDir=commands.getstatusoutput('echo $CMSSW_BASE')
    if baseDir[0]:
        print "Error, you haven't set CMSSW envirnment"
        exit()
    print 'current CMSSW env: {0}'.format(baseDir[1])
    return baseDir[1]

########################
# add parser to the code
########################
def addOption():
    import argparse
    parser = argparse.ArgumentParser(description='Hiiii')
    parser.add_argument(
            '--dir', '-d', type=str, default=defaultStorageFolder,
            help='folder to keep output files'
            )
    parser.add_argument(
            '--fileName', '-f', type=str, default='result',
            help='output file name'
            )
    parser.add_argument(
            '--filelist', '-l', type=str, default='',
            help='input relative filelist name'
            )
    parser.add_argument(
            '--input', '-i',type=str, default='',
            help='inputfile name'
            )
    parser.add_argument(
            '--num', '-n', type=int, default=0,
            help='number of files separated'
            )

    return parser.parse_args()

if __name__ == "__main__":
    import commands
    args=addOption()
    if args.num == 0:
        print 'Error, sep number needs to be separated!'
        exit()

    if not args.filelist and not args.input:
        print 'Error, you need to setup input filelist! [-i] or [-l]'
        exit()

    ipFileList=''
    if args.filelist:
        defaultPath=getCMSSWVersion() + '/src/histProduce/histProduce/python/{}_cfi.py'
        ipFileList=defaultPath.format(args.filelist)

    elif args.input:
        ipFileList=args.input
    if args.dir != defaultStorageFolder:
        status=commands.getstatus( 'ls {0}'.format(args.dir) )
        if status:
            print 'Error, output folder not found!'
            exit()
    else:
        commands.getstatus( 'mkdir {} -p'.format(defaultStorageFolder.format(USER)) )

    fLists=getRootFiles( ipFileList, args.num )
    Size=len(fLists)
    for idx in range(Size):
        fileListCreat( fLists[idx], '{0}_{1}'.format(args.fileName, idx), args.dir)


