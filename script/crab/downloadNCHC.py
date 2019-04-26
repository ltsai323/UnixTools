#!/usr/bin/env python
# this file load inputPath and to download files from remote site.
# inputPath comes from viewNCHC.py. the above is the example:
# /cms/store/user/ltsai/2016Data/treeData/Charmonium/treeData_2016RunC/180904_064826/0000/treeCreatingSpecificDecay_2017Data_1.root
# 
# usage:
#     ./thisFile.py -i path -d 2016RunC
#     ./thisfile.py -i path -d 2016RunC --site=se01.grid.nchc.org.tw --defaultPath=${HOME}/myDataStorage
REMOTESITE='se01.grid.nchc.org.tw'
DEFAULTPATH='${HOME}/Data/CRABdata'
DIROPTION='default'

import datetime
import argparse
import os, sys

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
    return parser.parse_args()


if __name__ == '__main__':
    args=addOption()
    if args.inputPath == '':
        print 'you need to use [-i] or [--inputPath] to select a file to download, or use [--help]'
        exit()

    storageFolder='CRABdata_{0}_{1}'.format(args.dirOption,datetime.datetime.now().date().strftime('%d_%m_%Y'))
    os.system( 'mkdir -p {}/{}'.format(args.defaultPath, storageFolder) )
    print 'file will storage at this folder : {}'.format(storageFolder)
    os.system( 'ls {}'.format(args.defaultPath) )

    with open( args.inputPath, 'r' ) as fLinks:
        for link in fLinks:
            os.system('xrdcp root://{0}/{1}  {2}/{3}/'.format(args.site, link.strip(), args.defaultPath, storageFolder) )
    print 'complete! your file is stored at {}/{}'.format(args.defaultPath, storageFolder)
    if args.stillRunning:
        os.system( 'cp {0} {1}/{2}/'.format(args.inputPath,args.defaultPath,storageFolder) )
