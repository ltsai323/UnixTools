#!/usr/bin/env python2
import csv
import re

totList={
        'pLbTk':None,
        'nLbTk':None,
        'pLbL0':None,
        'nLbL0':None,
        }
with open('log_calcSideband_fromFittedBackgroundShape.csv','r') as iFile:
    fRows=csv.DictReader(iFile)
    for fRow in fRows:
        totVal=0.
        totErr2=0.

        for key,val in fRow.iteritems():
            if re.match(r'[a-zA-Z0-9]+Val',key):
                totVal+=float(val)
            elif re.match(r'[a-zA-Z0-9]+Err',key):
                totErr2+=float(val)**2
            else:
                pass
                #print 'key:{0}, val:{1}'.format(key,val)
        totList[ fRow['channel'] ] = (totVal,totErr2)
print totList
pV =totList['pLbTk'][0]
pE2=totList['pLbTk'][1]
nV =totList['nLbTk'][0]
nE2=totList['nLbTk'][1]
fV =(pV-nV)/(pV+nV)
pV2=pV*pV
nV2=nV*nV
tV4=(pV+nV)*(pV+nV)*(pV+nV)*(pV+nV)
fE2=(pE2*4.*nV2+nE2*4.*pV2)/tV4
#fE2=pE2*4.*nV**2/(pV+nV)**4+nE2*4.*pV**2/(pV+nV)**4
print 'Acp LbTk = ({0:.3E},{1:.3E})'.format(fV,fE2**0.5)
pV =totList['pLbL0'][0]
pE2=totList['pLbL0'][1]
nV =totList['nLbL0'][0]
nE2=totList['nLbL0'][1]
fV =(pV-nV)/(pV+nV)
pV2=pV*pV
nV2=nV*nV
tV4=(pV+nV)*(pV+nV)*(pV+nV)*(pV+nV)
fE2=(pE2*4.*nV2+nE2*4.*pV2)/tV4
#fE2=pE2*4.*nV**2/(pV+nV)**4+nE2*4.*pV**2/(pV+nV)**4
print 'Acp LbL0 = ({0:.3E},{1:.3E})'.format(fV,fE2**0.5)
