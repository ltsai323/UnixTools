#!/usr/bin/env python2
# usage:
#    ./thisFile.py
# everytime you use this code, modify the content!
# if you put
#    preText="'file:"
#    endText="',"
#    the command to be written in file is
#
#    #!/usr/bin/env python2
#    fileList=[
#    'file:/myFile/To/Path',
#    'file:/myFile/To/Path2',
#    ]

# decide output file : fLink$$_cfi.py
fNameNumFrom=20
fNameNumTo=30
filePath='/home/ltsai/Data/bjob/MC_LbTk_180430/BPHSDecay/'
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

numToSep=fNameNumTo-fNameNumFrom
num=len(filePaths)/numToSep+1
for j in range(numToSep):
    fileLink=[ filePaths[i] for i in range( j*num, (j+1)*num ) if i < len(filePaths) ]
    writeFile=open( 'fLink{:02d}_cfi.py'.format(j+fNameNumFrom), 'w' )
    writeFile.write( '#!/usr/bin/env python2\n' )
    writeFile.write( 'fileLinks=[\n' )

    # write the content in file
    for fLink in fileLink:
        writeFile.write( '{0}{1}{2}\n'.format( preText, fLink, endText ) )
    writeFile.write(']\n')
    writeFile.close()

