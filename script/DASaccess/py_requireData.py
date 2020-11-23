#!/usr/bin/env python2
# minimal usage:
#  ./this.py -d 2016RunH --execute
# maximal usage:
#  ./this.py -d 2016RunH --execute -s myCustomDAS_CLIENT.sh --memo=hihihihi --cmsversion=94X
# where "datasearch.sh" script must have command(s) like 
#    das_client --query="file dataset=/a/b/c"
defaultPath='${{HOME}}/ReceivedFile/DATA/CMSData/'
defaultCMSSW='CMSSW_9_4_14'
outPath=''
defaultOutputFileName='downloadScript_{label}{duplicateFix}.sh'

scriptContent='''#!/usr/bin/env sh
export XRD_NETWORKSTACK=IPv4
mkdir -p {MYstorage}
{MYcommand}
{MEMOCreat}
'''

mycommandTemplate='xrdcp root://cms-xrd-global.cern.ch/{filepath} {folder}/'


# add parser to the code
def addOption():
   import argparse
   parser = argparse.ArgumentParser(description='browse remote site by the number, open this python to get more detail usage.')
   parser.add_argument(
         '--dir', '-d', default=None, type=str,
         help='Necessary information. To add information to output directory. Date inofrmation would be attached.'
         )
   parser.add_argument(
         '--script', '-s', default='./datasearch.sh', type=str,
         help='change the script containing command "das_client --query=...", default uses  ./datasearch.sh'
         )
   parser.add_argument(
         '--memo', default=None, type=str,
         help='add additional information in memo'
         )
   parser.add_argument(
         '--cmsversion', '-v', default=defaultCMSSW, type=str,
         help='set the CMSSW version that you processed the file.'
         )
   parser.add_argument(
         '--execute', action='store_true',
         help='execute the output script after finished.'
         )
   return parser.parse_args()
# if empty or commented line, return None
def regularizeReceivedCommand(inStr):
   outStr=None
   line=inStr.strip() # remove spacee head and \n tail in thw string
   if not line: return outStr
   if line[0]=='#' : return outStr
   return line
# execute shell command and exit code once an error detected.
def runShellCommand(inCommand):
   res=commands.getstatusoutput(inCommand)
   if res[0] != 0:
      raise KeyError('--- error --- : command "{0}"\ngives a wrong output. The output is\n{1}'.format(inCommand,res[1]))
   return res[1].split('\n')



def checkPathExists(defaultPath):
   import os
   if not os.path.isdir(defaultPath):
      raise  SystemExit(
            '--- error --- : no default path found. you need to create the directory "{0}" to store the file.  And it is recommended to use "ln -s" to link the storage zone to your home directory'.format(defaultPath)
                  )

def checkArgs(args):
   if args.dir==None:
      print '--- error --- : you need to set up [-d][--dir] option, use [-h] option to check the detail'
      exit(1)

def checkExecCmds(cmd):
   if len(cmds)==0:
      print '--- error --- : no command found in the script'
      exit(2)

def collectCommandsFromFile(scriptFile):
   with open(scriptFile) as inScript:
      cmds=[]
      for sreadline in inScript.readlines():
         sline=regularizeReceivedCommand(sreadline)
         if not sline: continue
         cmds.append(sline)
      return cmds
   raise IOError('--- error --- : incoming script file {0} is not found! check [-s][--script] option again.'.format(scriptFile))

def recordResultToFile(cmdSource, dasLinkList, args, outHistory):
   print 'there are {0} good results found from command\n    [{1}]'.format(len(dasLinkList), cmdSource)
   outputLabel=cmdSource.split('/')[1]


   fixLabel= '.%d' % outHistory.count(outputLabel) if outputLabel in outHistory else ''
   outHistory.append(outputLabel)

   outfilename=defaultOutputFileName.format( label=outputLabel, duplicateFix=fixLabel)
   outfile=open(outfilename,'w')

   myfolder='{0}/{1}/{2}/{3}{4}'.format(defaultPath,args.cmsversion,args.dir,outputLabel,fixLabel)
   outfile.write(
      scriptContent.format(
         MYstorage=myfolder,
         MYcommand='\n'.join(
            [mycommandTemplate.format(filepath=dasLink,folder=myfolder) if dasLink else '' for dasLink in dasLinkList]
            ),
         MEMOCreat='echo -e "download command :\\n    {inputCommand}\\nmy memo : {MEMO}" > {folder}/memo.txt'.format(inputCommand=cmdSource,folder=myfolder, MEMO=args.memo)
         )
      )
   outfile.close()

import commands
if __name__ == "__main__":
   args=addOption()
   checkArgs(args)
   cmds=collectCommandsFromFile(args.script)

   checkExecCmds(cmds)

   outfileHistory=[]
   for cmd in cmds:
      resCollection=runShellCommand(cmd)
      recordResultToFile(cmd, resCollection, args, outfileHistory)
      if args.execute:
         os.system('sh {execFile}'.format(execFile=outfilename))
