#!/usr/bin/env python2
# minimal usage:
#  ./this.py -d vertexProducer --exec
# maximal usage:
#  ./this.py -d flashGG --exec -s myCustomDAS_CLIENT.sh -o customDWN.sh
#not used  # massive usage:
#not used  #  ./this.py -d hihi -s massiveDAS_CLIENT.sh // automatically use tag to classify output files.
_path='${{HOME}}/ReceivedFile/DATA/CMSData/{info}/'

scriptContent='''#!/usr/bin/env sh
export XRD_NETWORKSTACK=IPv4
mkdir -p {MYstorage}
{MYcommands}
echo "use the command to download the data:" > {MYstorage}/memo.txt
echo "{origCommand}" >> {MYstorage}/memo.txt
'''

linetemplate='xrdcp root://cms-xrd-global.cern.ch/{filepath} ~/ReceivedFile/DATA/{folder}'


# add parser to the code
def addOption():
    import argparse
    parser = argparse.ArgumentParser(description='browse remote site by the number, open this python to get more detail usage.')
    parser.add_argument(
            '--dirtag', '-d', default=crabdata, type=str,
            help='An word used to specify output directory. It is necessary information. Date inofrmation would be attached.'
            )
    parser.add_argument(
            '--script', '-s', default='./datasearch.sh', type=str,
            help='change the script containing command "das_client --query=...", default uses  ./datasearch.sh'
            )
    parser.add_argument(
            '--addMemo', default=None, type=str,
            help='add additional information in memo'
            )
    #parser.add_argument(
    #        '--output', '-o', default='downloadScript.sh', type=str,
    #        help='Output file name. Default using "downloadScript.sh"'
    #        )

    parser.add_argument(
            '--exec', action='store_true',
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
def execAndCheckShellCommand(inCommand):
    res=commands.getstatusoutput(inCommand)
    if res[0] != 0:
        print '--- error --- : there is an error while executing the das_client'
        print '--- error --- : Here is the message'
        print res[1]
        exit(1)
    return res[1]

# extract information from command. The incoming command should be:
#       das_client --query="dataset dataset=/Lambda*13TeV*/*/MINIAODSIM"
def extractCollectionEraInfo(inStr):
    # purify command to "dataset=/A/B/C
    step1=inStr[inStr.find('query'):-1]
    step2=step1[step1.find('dataset'):-1]
    step3=step2[0:step2.rfind(' ')]

    # purify dataset=/a/b/c -> b
    strs=step3.split('/')
    return strs[2]
def linetemplateAccomplish(outAddrs,foldername):
    addrs=outAddrs.split()
    newAddrs=[ linetemplate.format(filepath=outAddr,folder=foldername) for outAddr in outAddrs.split()]
    return '\n'.join(newAddrs)



import commands
if __name__ == "__main__":
    args=addOption()

    with open(args.script) as inScript:
        writeContents=[]
        for sreadline in inScript.readlines():
            sline=regularizeReceivedCommand(sreadline)
            if not sline: continue

            execline=execAndCheckShellCommand(sline)
            collectionEra=extractCollectionEraInfo(sline)
            writeContents.append( {'origCommand':sline,'era':collectionEra,'outAddrs':execline} )

        import datetime
        today=datetime.date.today()
        dateInfo='{0:%B}{0:%y}'.format(today)

        if len(writeContents)==1:
            foldername='{0}_{1}'.format(args.dirtag,dateInfo)
            outAddr=linetemplateAccomplish(writeContents[0]['outAddrs'],foldername)
            with open('download.sh','w') as f:
                f.write(scriptContent.format(
                    MYstorage=_path.format(info=foldername),
                    MYcommands=outAddr,
                    origCommand=writeContents[0]['origCommand']
                    )
                )
        else:
            for writeContent in writeContents:
                foldername='{0}_{1}_{2}'.format(args.dirtag,writeContent['era'],dateInfo)
                outAddr=linetemplateAccomplish(writeContent['outAddrs'],foldername)
                with open('download_{0}.sh'.format(writeContent['era']),'w') as f:
                    f.write(scriptContent.format(
                        MYstorage=_path.format(info=foldername),
                        MYcommands=outAddr,
                        origCommand=writeContent['origCommand']
                        )
                    )



