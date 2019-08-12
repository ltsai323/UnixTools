#!/usr/bin/env python2
# usage: ./thisFile.py --work --hour=3 --minutes=37

import json
from datetime import datetime, timedelta
import argparse
import os, sys
import commands
defaultFile='/home/ltsai/script/tools/log_timeRecord.json'

# format template
#newData = {}
#newData['play'] = []
#newData['play'].append( {
#            'date'; 20171008,
#            'timeFrom' : ,
#            'timeTo'   : ,
#            'duration' : ,
#            } )


def createTmpNewFile(jsonContent):
    with open('tmp.txt', 'w') as tmpFile:
        json.dump(jsonContent, tmpFile)
        print 'new content created!'

def moveToContent(myFileName):
    os.system( 'mv tmp.txt {0}'.format(myFileName) )
    print 'the new file {0} is created'.format(myFileName)

def appendData(inTag,inH,inM, ipFile):
    with open(ipFile) as f:
        data = json.load(f)

        currentTime=datetime.now()
        pastDate=currentTime-timedelta(hours=inH)-timedelta(minutes=inM)
        currDate=currentTime

        dates=int(currDate.strftime('%Y%m%d'))
        pastT=int(pastDate.strftime('%H%M'))
        currT=int(currDate.strftime('%H%M'))
        durT=int((datetime(2019,1,1,0,0,0)+timedelta(hours=inH)+timedelta(minutes=inM)).strftime('%H%M'))
        print 'date : {0}  , pastTime: {1} , current time : {2} , duration : {3}'.format(dates, pastT, currT, durT)

        data[inTag].append({
            'date': dates,
            'timeFrom' : pastT,
            'timeTo'   : currT,
            'duration' : durT,
            })

    if data == None:
        print 'nothing EROR!'
        exit()
    createTmpNewFile(data)
    moveToContent(ipFile)


def appendDataFromSpecificTime(inTag,inH,inM, fromTime, ipFile):
    with open(ipFile) as f:
        data = json.load(f)

        minuteFROM  =int(fromTime  )%100
        hourFROM    =int(fromTime/100)%100
        dayFROM     =int(fromTime/10000)%100
        monthFROM   =int(fromTime/1000000)%100
        yearFROM    =int(fromTime/100000000)%10000

        pastDate=datetime(yearFROM,monthFROM,dayFROM,hourFROM,minuteFROM,0)
        currDate=pastDate+timedelta(hours=inH)+timedelta(minutes=inM)

        dates=int(currDate.strftime('%Y%m%d'))
        pastT=int(pastDate.strftime('%H%M'))
        currT=int(currDate.strftime('%H%M'))
        durT=int((datetime(2019,1,1,0,0,0)+timedelta(hours=inH)+timedelta(minutes=inM)).strftime('%H%M'))
        print 'date : {0}  , pastTime: {1} , current time : {2} , duration : {3}'.format(dates, pastT, currT, durT)

        data[inTag].append({
            'date': dates,
            'timeFrom' : pastT,
            'timeTo'   : currT,
            'duration' : durT,
            })

    if data == None:
        print 'nothing EROR!'
        exit()
    createTmpNewFile(data)
    moveToContent(ipFile)

def newJSON(inFile):
    data = {}
    data['play'] = []
    data['work'] = []
    data['necessities'] = []
    data['sleep'] = []

    data['play'].append({
            'date': 19110101,
            'timeFrom' : 0,
            'timeTo'   : 0,
            'duration' : 0,
        })
    data['work'].append({
            'date': 19110101,
            'timeFrom' : 0,
            'timeTo'   : 0,
            'duration' : 0,
        })
    data['necessities'].append({
            'date': 19110101,
            'timeFrom' : 0,
            'timeTo'   : 0,
            'duration' : 0,
        })
    data['sleep'].append({
            'date': 19110101,
            'timeFrom' : 0,
            'timeTo'   : 0,
            'duration' : 0,
        })
    if os.path.isfile(inFile):
        print 'current file exist!  Abort program'
    with open(inFile, 'w') as outfile:
        json.dump(data, outfile)

def addOption():
    parser = argparse.ArgumentParser(description='record play time and work time and create statistics histogram')
    parser.add_argument('--play', action='store_true', help='record play time')
    parser.add_argument('--work', action='store_true', help='record work time')
    parser.add_argument('--need', action='store_true', help='record necessities time')
    parser.add_argument('--zzzz', action='store_true', help='record sleep time')
    parser.add_argument('--show', action='store_true', help='create the statistics histograms, rootenv is needed')
    parser.add_argument('--fromtime', type=int, default=None, help='if you want to add some event from history, the time format is yyyyMMddHHMM')
    parser.add_argument('--hour', '-H', type=int, default=0, help='set the time duartion')
    parser.add_argument('--min' , '-M', type=int, default=0, help='set the time duartion')
    parser.add_argument('--file', '-f', type=str, default=defaultFile, help='set inputFile name')
    parser.add_argument('--newfile', action='store_true', help='create new json file')
    return parser.parse_args()

if __name__ == '__main__':
    opts=addOption()

    if opts.newfile:
        newJSON(opts.file)
        exit()

    if not (opts.play or opts.work or opts.need or opts.zzzz or opts.show):
        print 'you need to see [--help] to use this code'
        print 'force ended'
        exit()

    if not opts.file:
        print 'use [--file] or [-f] to loadFiles'
    if opts.show:
        print 'this function not completed'
        exit()

    if not opts.fromtime:
        if opts.play and opts.work:
            print 'error! you cannot set [--play] and [--work] at the same time'
        elif opts.play:
            appendData('play', opts.hour, opts.min, opts.file)
        elif opts.work:
            appendData('work', opts.hour, opts.min, opts.file)
        elif opts.need:
            appendData('necessities', opts.hour, opts.min, opts.file)
        elif opts.zzzz:
            appendData('sleep', opts.hour, opts.min, opts.file)
    else:
        if opts.play and opts.work:
            print 'error! you cannot set [--play] and [--work] at the same time'
        elif opts.play:
            appendDataFromSpecificTime('play', opts.hour, opts.min, opts.fromtime, opts.file)
        elif opts.work:
            appendDataFromSpecificTime('work', opts.hour, opts.min, opts.fromtime, opts.file)
        elif opts.need:
            appendDataFromSpecificTime('necessities', opts.hour, opts.min, opts.fromtime, opts.file)
        elif opts.zzzz:
            appendDataFromSpecificTime('sleep', opts.hour, opts.min, opts.fromtime, opts.file)

