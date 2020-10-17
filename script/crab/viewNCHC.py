#!/usr/bin/env python2
# this pyhon file mainly execute the command many times:
#    xrdfs se01.grid.nchc.org.tw ls /cms/store/user/ltsai/???
# to get crab data
# and the result is put in ./path.txt
# normal usage:
#   ./thisFile.py -u ltsai
# or
#   ./thisFile.py -i myPath.txt    where myPath.txt owns the content '/cms/store/user/myFile/Charmonium/'
# or
#   ./thisFile.py -i /cms/store/user/myFile/Charmonium/

# the output result would be
# not terminated:
#    /cms/store/user/myFile/Charmonium/2016RunH/190718/0000/tree_0.root
#    /cms/store/user/myFile/Charmonium/2016RunH/190718/0000/tree_1.root
# terminated:
#    /cms/store/user/myFile/Charmonium/


# enormous usage:
#     This usage is used get lists from lots of dataset.
#     By edit the output txt file and input the file again to get lots of output list.
#        ./thisFile.py -i myPath.txt
#                   where myPath.txt should have the contents:
#                        myName1,/cms/store/user/myFile/Charmonium/2016RunH/190718/0000/
#                        myName2,/cms/store/user/myFile/Charmonium/2016RunG/190718/0000/
#                        myName3,/cms/store/user/myFile/Charmonium/2016RunF/190718/0000/
#                        myName4,/cms/store/user/myFile/Charmonium/2016RunE/190718/0000/
#        'myName1' would be the output file name as 'path_myName1.txt'
#        This example would generate 4 output files.
#        To get the content after 'myName1', you need to see the next illustration

# if you want to use [-i][--input] to input a file, there needs to be a '.txt' in name
# or it would be recognized as a path in remote site.

# in the selection, you can use 'q/Q/0' to quit this program and record current list.
# you also can use 'L' to list all sub-directories under current list.
# ('L' option is related to [-i] option)

# if you want to select lots of link file. you can also use
#     ./thisFile.py -i   outName,/cms/store/user/myFile/Charmonium/2016RunH/190718/0000/

REMOTESITE='se01.grid.nchc.org.tw'
USER='ltsai'

import os,sys
import re
import commands
import argparse

class RemoteLS:
    def __init__( self, remoteSite, user, listAllFiles = False, outFile='path.txt', remotePath = '' ):
        self.__site = remoteSite
        self.__user = user
        self.__path = remotePath
        self.__file = outFile
        self.__lAll = listAllFiles
        self.resultPaths=[]
    def __del__(self):
        self.saveIt()
    def listAll(self):
        return self.__lAll
    def UpdateOutput(self, oName):
        self.__file=oName
    def getOutputFileName(self):
        return self.__file
    def clearWorkspace(self):
        outfile=open('./{0}'.format(self.__file), 'w')
        outfile.close()

    def writeListToResFile(self, pathList):
        outfile=open('./{0}'.format(self.__file), 'a')
        while path in pathList:
            outfile.write( path+'\n' )
        outfile.close()

    def targetFOUND(self, inPaths):
        out=re.match(r'.+/0000', inPaths)
        return out


######################################################################
# load path_ and execute 'xrdfs' command to record the return strings.
######################################################################
    def viewFile( self, path ):
        output=[]
        if path == '':
            output=commands.getstatusoutput( 'xrdfs {0} ls /cms/store/user/{1}'.format(self.__site, self.__user) )
        else:
            output=commands.getstatusoutput( 'xrdfs {0} ls {1}'.format(self.__site, path) )
        if output[0] != 0 or output[1] == '':
            return None
        else:
            return output[1].split() # return a list, separted with space.

###########################
# write the lists into file
###########################
    def saveTmpResult( self, resList ):
        myFile=open('./tmpPath.txt', 'w') # new line, if file exists, overwrite it.

        # save each line in input list
        for content in resList:
            myFile.write( content+'\n' )
        myFile.close()
    def removeTmpResult(self):
        myFile=open('./tmpPath.txt', 'w')
        myFile.close()
        commands.getoutput('rm ./tmpPath.txt')




##################################################
# open a txt file to record the output root files.
##################################################
    def saveIt( self ):
        outFile=open('./{0}'.format(self.__file), 'a')
        for res in self.resultPaths:
            outFile.write( res+'\n' )
        outFile.close()
    def recordPath( self, path ):
        self.resultPaths.append(path)

#####################################################
# two algorithm to search & record path to record
#####################################################

#######################################
# list all root file from the path list
#######################################
def recordRootResult( myClass, path ):
#    print 'check point recordRootResult 01 --- path = {0}'.format(path)
    filepaths=myClass.viewFile(path)
#    print 'check point recordRootResult 02 --- filepaths = {0}'.format(filepaths)
    if filepaths is None:
        return
#    print 'check point recordRootResult 03 --- filepath={0}'.format(filepaths)
    for content in filepaths:
#        print 'check point recordRootResult 03.01'
        mode=re.search(r'\w+\.root', content)
#        print 'check point recordRootResult 03.02'
        if not mode:
#            print 'check point recordRootResult 03.02.continue --' + content
            continue
#        print 'check point recordRootResult 03.03'
        myClass.recordPath(content)
#        print 'check point recordRootResult 03.04'
#    print 'check point recordRootResult end'

#######################################
# list all root file from the path list
#######################################
def recordAllResult( myClass, path ):
    #print 'recordAllResult: find {0}'.format(path)

    # search for word with "."
    mode = re.search(r'\w+\.\w+', path)
    if mode:
        myClass.recordPath(path)
        return

    # if this is a folder, check for its subDir
    checkPoint=myClass.viewFile(path)
    if checkPoint is None:
        myClass.recordPath(path)
    else:
        for path_1 in checkPoint:
            recordAllResult( myClass, path_1 )
#####################################################
# two algorithm to search & record path to record end
#####################################################


########################################
# save all results recoreded in pathList
########################################
def saveResult( myClass, pathList ):
#    print 'check point in saveResult 01 pathList={0}'.format(pathList)
    if myClass.listAll():
#        print 'check point in saveResult 02'
        for path in pathList:
            recordAllResult( myClass, path )
#        print 'check point in saveResult 02.01'
    else:
#        print 'check point in saveResult 03'
        if isinstance(pathList, list):
            for path in pathList:
                recordRootResult( myClass, path )
        elif isinstance(pathList, str):
            recordRootResult( myClass, pathList )
#        print 'check point in saveResult 03.01'



##################################################################
# give a initial path, to display what is contained in the folder,
# and ask user which folder want to enter.
##################################################################
def loopForSearchContent( myClass, initPath='' ):
#    print 'check point in loop 01 initPath={0}'.format(initPath)
    searchFolder=initPath
    if  myClass.targetFOUND(searchFolder):
#        print 'check point in loop 01.01'
        saveResult(myClass, searchFolder)
#        print 'check point in loop 01.02'
        exit()
#    print 'check point in loop 02'

    print '\n\ntmp result is recorded in (./tmpPath.txt)\n\n'
    while True:
#        print 'check point in loop 03'

        # receive the return from 'xrdfs ls'
        outList=myClass.viewFile( searchFolder )

#        print 'check point in loop 04'
        # write the results to file
        myClass.saveTmpResult(outList)
#        print 'check point in loop 05'

        isTargetDirectory=myClass.targetFOUND(outList[0])

        # keep choosing the directory
        if not isTargetDirectory:
            print 'please input a number to enter a folder, L to list all of sub-directory, or input q/Q/0 to quit'
            for id_, val in enumerate(outList):
                print '    ', id_+1, '. ', val
            myChosen=str( raw_input('your choice: ') )

            # quit this program, record current directory
            if myChosen == 'q' or myChosen == 'Q' or myChosen=='0':
                print 'your temporary result is stored in ./tmpPath.txt'
                exit()

            # if it is needed to list all sub-directory under current directory.
            elif myChosen == 'L':
                print 'print all sub-directory in current directory to the file {0}'.format(myClass.getOutputFileName())
                listedDirs=[]           # record ended paths
                tmplisteddirs=outList   # record not finished paths
                while tmplisteddirs:
                    currentdir=tmplisteddirs[0]
                    tmplisteddirs.remove(currentdir)
                    tmpOut=myClass.viewFile(currentdir)

                    finalDir=myClass.targetFOUND(tmpOut[0])

                    if finalDir:
                        listedDirs.extend(tmpOut)
                    else:
                        tmplisteddirs.extend(tmpOut)

                if myClass.getOutputFileName() == 'path.txt':
                    print 'Warning: output file name not set! choose new name?        (n/N) to default output name "path.txt"'
                    myChosen=str( raw_input('your choice: ') )
                    if not myChosen=='n' and not myChosen=="N":
                        myClass.UpdateOutput(myChosen+'.txt')

                with open(myClass.getOutputFileName(), 'w') as listedFile:
                    for out in listedDirs:
                        listedFile.write( out+'\n' )

                print 'Here is your folders to record all of lists (./{0})'.format(myClass.getOutputFileName())
                myClass.removeTmpResult()
                exit()



            try:
                searchFolder=outList[ int(myChosen)-1 ]
            except ValueError:
                print 'get a strange input'
                exit()

        # target directory found, start to deal with what to store in file.
        if isTargetDirectory:
        # analyze if this code needs to stop automatically.
        # if you don't need log and failed files. stop at 0000 & print 0000/?.root
        # if you need all files, you will get
        #    0000/?.root, 0000/failed/?, 0000/log/?

            myClass.clearWorkspace()
            saveResult(myClass, outList)

            print 'Here is your folders to record files (./{0})'.format(myClass.getOutputFileName())
            print 'Recording relative files in these folders, please wait!'
            myClass.removeTmpResult()
            exit()


# add parser to the code
def addOption():
    parser = argparse.ArgumentParser(description='browse remote site by the number, open this python to get more detail usage.')
    parser.add_argument(
            '--input', '-i', type=str, default='',
            help='input a initial path to be read in the server'
            )
    parser.add_argument(
            '--site', '-s', type=str, default=REMOTESITE,
            help='decide where you want to get data'
            )
    parser.add_argument(
            '--user', '-u', type=str, default=USER,
            help='decide the user folder'
            )
    parser.add_argument(
            #'--listAllFiles', '-l', type=bool, default=False, action='store_true',
            '--listAllFiles', '-l',action='store_true',
            help='list all files, not only root files not failed.'
            )
    return parser.parse_args()



if __name__ == '__main__':
    args=addOption()
    currentUSER=commands.getoutput( 'echo $USER' )
    if currentUSER != 'ltsai' and args.user == USER:
        print 'Use [-u][--user] to select user in NCHC. Also, you can check [--help] for information.'
        exit()

    mainControler=RemoteLS(
            remoteSite=args.site,
            user=args.user,
            listAllFiles=args.listAllFiles,
            outFile='path.txt',
            remotePath=args.input,
            )
    try:
        if '.txt' in args.input:
            print 'Message: recognize input as a file'
            inputFile=open(args.input, 'r')
            initContent=inputFile.read().split()
            if len(initContent) is not 1:
                print '----ERROR----: input file has wrong format, check the content. It needs to be only 1 line.'
                exit()
            loopForSearchContent( mainControler, initContent[0] )
        else:
            print 'Message: recognize input as a path in remote dir'
            if ',' not in args.input:
                print 'Message: dir = {0}'.format(args.input)
                loopForSearchContent( mainControler, args.input )
            else:
                fName='path_'+args.input.split(',')[0]+'.txt'
                pName=args.input.split(',')[1]
                print 'Message: output file = {0}'.format(fName)
                print 'Message: dir = {0}'.format(pName)
                mainControler.UpdateOutput(fName)
                print 'test point a'
                loopForSearchContent( mainControler, pName )
                print 'test point b'

    except IOError:
        loopForSearchContent( mainControler, '' )


# xrdfs se01.grid.nchc.org.tw ls /cms/store/user/ltsai/??? > path.txt
# main targeet:
#     show the folders and use the selection by keyboard to get files in command 'xrdfs'

# analyze the output of the string, is folder or file.
