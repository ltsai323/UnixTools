#!/usr/bin/env python
# this file load inputPath and to download files from remote site.
# inputPath comes from viewNCHC.py. the above is the example:
# /cms/store/user/ltsai/2016Data/treeData/Charmonium/treeData_2016RunC/180904_064826/0000/treeCreatingSpecificDecay_2017Data_1.root
# 
# usage:
#     ./thisFile.py -i path -d 2016RunC
#     ./thisfile.py -i path -d 2016RunC --site=se01.grid.nchc.org.tw --defaultPath=${HOME}/myDataStorage
# The executed command is:
#       xrdcp root://se01.grid.nchc.org.tw//cms/store/user/ltsai/2016Data/treeData/Charmonium/treeData_2016RunC/180904_064826/0000/treeCreatingSpecificDecay_2017Data_1.root myLocalFolder/

import datetime
import argparse
import os, sys
import commands

__home=commands.getoutput('echo $HOME')
REMOTESITE='se01.grid.nchc.org.tw'
DEFAULTPATH=__home+'/Data/CRABdata'
DIROPTION='default'
FAILEDLOG='log_failedDownload.log'


# add parser to the code
def addOption():
    parser = argparse.ArgumentParser(description='load inputPath to download files from remote site')
    parser.add_argument(
            '--inputPath', '-i', type=str, default='',
            help='input path file record NCHCpaths'
            )
    parser.add_argument(
            '--site', type=str, default=REMOTESITE,
            help='where to get remote data'
            )
    parser.add_argument(
            '--defaultPath', type=str, default=DEFAULTPATH,
            help='default path to store remote data'
            )
    parser.add_argument(
            '--dirOption', '-d', type=str, default=DIROPTION,
            help='option name to be put on folder name'
            )
    parser.add_argument(
            '--stillRunning', '-s', action='store_true',
            help='option for the jobs is still running, use this option to copy the path file to output directory'
            )
    parser.add_argument(
            '--createDefaultPath',action='store_true'
            )
    return parser.parse_args()

if __name__ == '__main__':
    args=addOption()
    if args.inputPath == '':
        print 'you need to use [-i] or [--inputPath] to select a file to download, or use [--help]'
        exit()
    defPath=args.defaultPath
    if args.createDefaultPath:
        'still use default path'
        pass
    elif not os.path.exists(args.defaultPath) or not os.path.isdir(args.defaultPath):
        print '-------Warning : default path not found! turn to use current directory'
        defPath='.'

    print 'default path = ' + defPath
    storageFolder='CRABdata_{0}_{1}'.format(args.dirOption,datetime.datetime.now().date().strftime('%d_%m_%Y'))
    os.system( 'mkdir -p {0}/{1}'.format(defPath, storageFolder) )
    print 'file will storage at this folder : {0}'.format(storageFolder)

    failedLog=open(FAILEDLOG,'a')

    with open( args.inputPath, 'r' ) as inFile:
        fLinks=inFile.read().split('\n')

        for idx,link in enumerate(fLinks):
            if 'root' in link:
                sys.stdout.write('\rProcessing files %d in %d' % (idx, len(fLinks)))
                sys.stdout.flush()
                #os.system('xrdcp root://{0}/{1}  {2}/{3}/'.format(args.site, link.strip(), defPath, storageFolder) )
                res=commands.getstatusoutput('xrdcp root://{0}/{1}  {2}/{3}/'.format(args.site, link.strip(), defPath, storageFolder) )
                if res[0]:
                    failedMessage='''
############ an error found ##################
## input path = {pathInfo}
## command: xrdcp root://{rSite}/{rPath} {lPath0}{lPath1}
## messages : {msg}
##############################################

'''
                    failedLog.write( failedMessage.format(pathInfo=link.strip(), msg=res[1],rSite=args.site,rPath=link.strip(),lPath0=defpath,lPath1=storageFolder) )
                    print '''
############ an error found #################
## input path = {pathInfo}
## messages : {msg}
##############################################

'''.format(pathInfo=link.strip(),msg=res[1])
    if args.stillRunning:
        os.system( 'cp {0} {1}/{2}/'.format(args.inputPath,defPath,storageFolder) )
    failedLog.close()
    print '''
complete! your file is stored at {0}/{1}

'''.format(defPath, storageFolder)
