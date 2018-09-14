#!/usr/bin/env python

import os
import commands
import argparse
defaultStorageFolder='/home/ltsai/Data/qjob/qSubResult'
defaultMessageFolder='/home/ltsai/Data/qjob/qSubMessage'
defaultErrorFolder  ='/home/ltsai/Data/qjob/qSubMessage'


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
        print 'qSub storage folder:'
        res1=commands.getstatusoutput( 'ls {}/*'.format(defaultStorageFolder) )
        if res1[0] == 0:
            for message in res1[1].split():
                print '    {}'.format(message)
        else:
            print '    there is nothing in qSub storage folder'

        print 'qSub message folder:'
        res2=commands.getstatusoutput( 'ls {}/*'.format(defaultMessageFolder) )
        if res2[0] == 0:
            for message in res2[1].split():
                print '    {}'.format(message)
        else:
            print '    there is nothing in qSub message folder'
        print 'qSub error folder:'
        res3=commands.getstatusoutput( 'ls {}/*'.format(defaultErrorFolder) )
        if res3[0] == 0:
            for message in res3[1].split():
                print '    {}'.format(message)
        else:
            print '    there is nothing in qSub error folder'

        print '\nif you want to delete all of them, use [--delete] option'

