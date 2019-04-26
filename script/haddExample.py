#!/usr/bin/env python

import commands
numToSep=30

files=commands.getoutput('ls somewhere').split()

N=len(files)/numToSep
fTmpLists=['']*(N+1)

i=0
j=0
for file in files:
    fTmpLists[j]='{} {}'.format(fTmpLists[j], file)
    i+=1
    if i==N:
        i=0
        j+=1

fTmps=''
for idx in range(N+1):
    commands.getstatus('hadd /tmp/ltsai/tmpFile_{:02}.root {}'.format(idx, fTmpLists[idx]))
    fTmps+=' /tmp/ltsai/tmpFile_{:02}.root'.format(idx)
commands.getstatus('hadd total.root {}'.format(fTmps))




