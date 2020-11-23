#!/usr/bin/env python

import os
import commands
import argparse
defaultStorageFolder='/afs/cern.ch/user/l/ltsai/Work/jobSummary/condor/output'
defaultMessageFolder='/afs/cern.ch/user/l/ltsai/Work/jobSummary/condor/stdout'
defaultErrorFolder  ='/afs/cern.ch/user/l/ltsai/Work/jobSummary/condor/errors'


# add parser to the code
def addOption():
    parser = argparse.ArgumentParser(description='This is the code to execute "rm -r myDir" to remote site')
    parser.add_argument(
            '--delete', action='store_true',
            help='confirm you really want to delete files'
            )
    return parser.parse_args()

if __name__ == '__main__':
    args=addOption()
    if args.delete:
        print 'start to clean storage directory:'
        os.system( '/bin/rm -r {}/*'.format(defaultStorageFolder) )
        print 'start to clean output directory:'
        os.system( '/bin/rm -r {}/*'.format(defaultMessageFolder) )
        print 'start to clean error directory:'
        os.system( '/bin/rm -r {}/*'.format(defaultErrorFolder) )
        print 'Finished'
    else:
        print 'qjob working directory owns:'
        print 'condor job storage folder:'
        res1=commands.getstatusoutput( 'ls {}/*'.format(defaultStorageFolder) )
        if res1[0] == 0:
            for message in res1[1].split():
                print '    {}'.format(message)
        else:
            print '    there is nothing in condor job storage folder'

        print 'condor job message folder:'
        res2=commands.getstatusoutput( 'ls {}/*'.format(defaultMessageFolder) )
        if res2[0] == 0:
            for message in res2[1].split():
                print '    {}'.format(message)
        else:
            print '    there is nothing in condor job message folder'
        print 'condor job error folder:'
        res3=commands.getstatusoutput( 'ls {}/*'.format(defaultErrorFolder) )
        if res3[0] == 0:
            for message in res3[1].split():
                print '    {}'.format(message)
        else:
            print '    there is nothing in condor job error folder'

        print '\nif you want to delete all of them, use [--delete] option'


