#!/usr/bin/env python2
# this pyhon file mainly execute the command many times:
#    xrdfs se01.grid.nchc.org.tw ls /cms/store/user/ltsai/???
# to get crab data
# and the result is put in ./path
REMOTESITE='se01.grid.nchc.org.tw'
USER='ltsai'

import os,sys
import re
import commands
import argparse

class RemoteLS:
    def __init__( self, remoteSite, user, listAllFiles = False, outFile='path', remotePath = '' ):
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
    def clearWorkspace(self):
        outfile=open('./{0}'.format(self.__file), 'w')
        outfile.close()

    def writeListToResFile(self, pathList):
        outfile=open('./{0}'.format(self.__file), 'a')
        while path in pathList:
            outfile.write( path+'\n' )
        outfile.close()


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
        myFile=open('./tmpPath', 'w') # new line, if file exists, overwrite it.

        # save each line in input list
        for content in resList:
            myFile.write( content+'\n' )
        myFile.close()
    def removeTmpResult(self):
        myFile=open('./tmpPath', 'w')
        myFile.close()
        commands.getoutput('rm ./tmpPath')




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
    filepaths=myClass.viewFile(path)
    if filepaths is None:
        return
    for content in filepaths:
        mode=re.search(r'\w+\.root', content)
        if not mode:
            continue
        myClass.recordPath(content)

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
    if myClass.listAll():
        for path in pathList:
            recordAllResult( myClass, path )
    else:
        for path in pathList:
            recordRootResult( myClass, path )



##################################################################
# give a initial path, to display what is contained in the folder,
# and ask user which folder want to enter.
##################################################################
def loopForSearchContent( myClass, initPath='' ):
    searchFolder=initPath
    print '\n\ntmp result is recorded in (./tmpPath)\n\n'
    while True:
        # receive the return from 'xrdfs ls'
        outList=myClass.viewFile( searchFolder )

        # write the results to file
        myClass.saveTmpResult(outList)

        isTargetDirectory=re.match(r'.+/0000', outList[0])

        # keep choosing the directory
        if not isTargetDirectory:
            print 'please input a number to enter a folder, or input q/Q/0 to quit'
            for id_, val in enumerate(outList):
                print '    ', id_+1, '. ', val
            myChosen=str( raw_input('your choice: ') )
            if myChosen == 'q' or myChosen == 'Q' or myChosen=='0':
                print 'your temporary result is stored in ./tmpPath'
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

            print 'Here is your folders to record files (./path)'
            print 'Recording relative files in these folders, please wait!'
            myClass.removeTmpResult()
            exit()


# add parser to the code
def addOption():
    parser = argparse.ArgumentParser(description='browse remote site by the number')
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
    mainControler=RemoteLS(
            remoteSite=args.site,
            user=args.user,
            listAllFiles=args.listAllFiles,
            outFile='path',
            remotePath=args.input,
            )
    try:
        inputFile=open(args.input, 'r')
        initContent=inputFile.read().split()
        if len(initContent) is not 1:
            print 'input file has wrong format, check the content. It needs to be only 1 line.'
            exit()
        loopForSearchContent( mainControler, initContent[0] )
    except IOError:
        loopForSearchContent( mainControler, '' )


# xrdfs se01.grid.nchc.org.tw ls /cms/store/user/ltsai/??? > path
# main targeet:
#     show the folders and use the selection by keyboard to get files in command 'xrdfs'

# analyze the output of the string, is folder or file.

