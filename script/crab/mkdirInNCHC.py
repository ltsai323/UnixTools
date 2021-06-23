#!/usr/bin/env python
# this pyhon file mainly execute the command:
#    xrdfs se01.grid.nchc.org.tw mkdir /cms/store/user/ltsai/mySelectedPath
# usage:
#  1. To check the directory structure in specific directory
#    ./this.py -l --dir=crabtest
#  2. To make a new directory
#    ./this.py --dir=crabtest/newDir
REMOTESITE='se01.grid.nchc.org.tw'
USER='ltsai'

import commands
import argparse

# add parser to the code
def addOption():
    parser = argparse.ArgumentParser(description='execute "mkdir" commands to remote site.')
    parser.add_argument(
            '--dir', '-d', type=str, default='',
            help='new dir need to be created to remote'
            )
    parser.add_argument(
            '--site', '-s', type=str, default=REMOTESITE,
            help='decide where to create directory'
            )
    parser.add_argument(
            '--user', '-u', type=str, default=USER,
            help='decide the user folder'
            )
    parser.add_argument(
            '--list', '-l', action='store_true',
            help='list selected directory'
            )
    return parser.parse_args()

if __name__ == "__main__":
    args = addOption()

    # open list mode, only list current directory from remote, then end of the program
    if args.list:
        output=commands.getstatusoutput( 'xrdfs {0} ls /cms/store/user/{1}/{2}'.format(args.site, args.user, args.dir) )
        print 'current dir: [{0}] owns:'.format( '/cms/store/user/{0}/{1}'.format(args.user, args.dir) )
        print output[1]
        exit()

    if args.dir == '':
        print 'you need to use [-d] or [--dir] option t to make a new directory\n'
        print 'futher information, using [--help] option.'
        exit()
    if args.dir[0] == '/':
        output=commands.getstatusoutput( 'xrdfs {0} mkdir /cms{1}'.format(args.site, args.dir) )
    else:
        output=commands.getstatusoutput( 'xrdfs {0} mkdir /cms/store/user/{1}/{2}'.format(args.site, args.user, args.dir) )
    if output[0] == 0:
        print "sucess to create new directory :"
        print "/cms/store/user/{0}/{1}".format(args.user,args.dir)
    else:
        print "failed! the error is"
        print output[1]

