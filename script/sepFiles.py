#!/usr/bin/env python2
# usage:
#    ./thisFile.py
# everytime you use this code, modify the content!
# if you put
#    preText='scp ntu:'
#    endText=' myPath'
#    the command to be written is------ scp ntu:/calc/Path/File myPath

numToSep=20
filePath='/home/ltsai/Data/bjob/MC_LbTk_180430/'
fileType='root'

preText="'file:"
endText="',"


import commands
import os
fileInfo=commands.getstatusoutput( 'ls {0}*.{1}'.format(filePath, fileType) )
if fileInfo[0]:
    print 'input wrong file path!'
    exit(1)
filePaths=fileInfo[1].split('\n')
print len(filePaths)
num=len(filePaths)/numToSep+1
for j in range(numToSep):
    fileLink=[ filePaths[i] for i in range( j*num, (j+1)*num ) if i < len(filePaths) ]
    writeFile=open( 'fLink{:02d}_cfi.py'.format(j), 'w' )
    writeFile.write( '#!/usr/bin/env python2\n' )
    writeFile.write( 'fileLinks=[\n' )
    for fLink in fileLink:
        writeFile.write( '{0}{1}{2}\n'.format( preText, fLink, endText ) )
    writeFile.write(']\n')
    writeFile.close()

