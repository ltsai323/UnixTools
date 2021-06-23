#!/usr/bin/env python
# fit LbL0, LbLo in data and MC.
# use MC shape to determine the number in data.
# finalize Lambda0 cut for better fitting result.

from ROOT import TLegend
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsReal
import os

import csv

dataFileL0='result_flatNtuple_LbL0_preSelection_noKinematicCut.root'
dataFileTk='result_flatNtuple_LbTk_preSelection_noKinematicCut.root'
outLog='log_calcSideband_eventExcludeSignalRegion'
signalRegion=[5.54,5.70]
ptRegion=[
        [20,30,'20To30'],
        [30,33,'30To33'],
        [33,38,'33To38'],
        [38,45,'38To45'],
        [45,500,'45Tinf'],
        ]

space=RooWorkspace('space',False)
space.factory('lbl0Mass[5.4,5.9]')
space.factory('lbtkMass[5.4,5.9]')
space.factory('lbtkbarMass[5.4,5.9]')
space.factory('lbl0Pt[20.,500.]')
space.factory('lbtkPt[20.,500.]')
space.factory('tktkMass[0.5,2.0]')

writeColumn=[
        'channel',
        '20To30Val','20To30Err',
        '30To33Val','30To33Err',
        '33To38Val','33To38Err',
        '38To45Val','38To45Err',
        '45TinfVal','45TinfErr',
        ]
columnIdx={ name:idx for idx,name in enumerate(writeColumn) }
#ft=open(outLog+'.txt','w')
fc=open(outLog+'.csv','w')
cwrite=csv.writer(fc)
cwrite.writerow(writeColumn)
pLbL0Rec=[ None for i in writeColumn ]
nLbL0Rec=[ None for i in writeColumn ]
pLbTkRec=[ None for i in writeColumn ]
nLbTkRec=[ None for i in writeColumn ]
pLbL0Rec[0]='pLbL0'
nLbL0Rec[0]='nLbL0'
pLbTkRec[0]='pLbTk'
nLbTkRec[0]='nLbTk'

load2016Data=True
if load2016Data:
    checkpLbL0=True
    checknLbL0=True
    checkpLbTk=True
    checknLbTk=True

    inFileL0=TFile.Open(dataFileL0)
    inFileTk=TFile.Open(dataFileTk)
    inpLbL0=inFileL0.Get('pLbL0/2016Data')
    innLbL0=inFileL0.Get('nLbL0/2016Data')
    inpLbTk=inFileTk.Get('pLbTk/2016Data')
    innLbTk=inFileTk.Get('nLbTk/2016Data')

    massLbL0=space.var('lbl0Mass')
    masspLbTk=space.var('lbtkMass')
    massnLbTk=space.var('lbtkbarMass')
    massTkTk=space.var('tktkMass')
    LbL0Pt=space.var('lbl0Pt')
    LbTkPt=space.var('lbtkPt')

    loadDatasetpLbL0=RooDataSet('loadData16pLbL0','loadData16',inpLbL0,RooArgSet(massLbL0,massTkTk,LbL0Pt))
    loadDatasetnLbL0=RooDataSet('loadData16nLbL0','loadData16',innLbL0,RooArgSet(massLbL0,massTkTk,LbL0Pt))
    loadDatasetpLbTk=RooDataSet('loadData16pLbTk','loadData16',inpLbTk,RooArgSet(masspLbTk,LbTkPt))
    loadDatasetnLbTk=RooDataSet('loadData16nLbTk','loadData16',innLbTk,RooArgSet(massnLbTk,LbTkPt))



    #tktkMassCut='tktkMass>1.100&&tktkMass<1.120'
    tktkMassCut='tktkMass>1.105&&tktkMass<1.125'
    #tktkMassCut='tktkMass>1.110&&tktkMass<1.120'
    for ptRange in ptRegion:
        rName=ptRange[2]
        pLbL0Num=0
        nLbL0Num=0
        pLbTkNum=0
        nLbTkNum=0
        if checkpLbL0:
            binData=loadDatasetpLbL0.reduce(tktkMassCut+'&&lbl0Pt>{0}.&&lbl0Pt<{1}.'.format(ptRange[0],ptRange[1]))
            pLbL0Num=binData.sumEntries()
        if checknLbL0:
            binData=loadDatasetnLbL0.reduce(tktkMassCut+'&&lbl0Pt>{0}.&&lbl0Pt<{1}.'.format(ptRange[0],ptRange[1]))
            nLbL0Num=binData.sumEntries()
        if checkpLbTk:
            binData=loadDatasetpLbTk.reduce('lbtkPt>{0}.&&lbtkPt<{1}.'.format(ptRange[0],ptRange[1]))
            pLbTkNum=binData.sumEntries()
        if checknLbTk:
            binData=loadDatasetnLbTk.reduce('lbtkPt>{0}.&&lbtkPt<{1}.'.format(ptRange[0],ptRange[1]))
            nLbTkNum=binData.sumEntries()

        pLbL0Rec[ columnIdx[rName+'Val'] ]=int(pLbL0Num)
        pLbL0Rec[ columnIdx[rName+'Err'] ]=int(pLbL0Num**0.5)
        nLbL0Rec[ columnIdx[rName+'Val'] ]=int(nLbL0Num)
        nLbL0Rec[ columnIdx[rName+'Err'] ]=int(nLbL0Num**0.5)
        pLbTkRec[ columnIdx[rName+'Val'] ]=int(pLbTkNum)
        pLbTkRec[ columnIdx[rName+'Err'] ]=int(pLbTkNum**0.5)
        nLbTkRec[ columnIdx[rName+'Val'] ]=int(nLbTkNum)
        nLbTkRec[ columnIdx[rName+'Err'] ]=int(nLbTkNum**0.5)

    #ft.write('pLbL0 sideband in range {1}, (yield,error) = {0}\n'.format(bkgYield, rName) )
    cwrite.writerow(pLbL0Rec)
    cwrite.writerow(nLbL0Rec)
    cwrite.writerow(pLbTkRec)
    cwrite.writerow(nLbTkRec)
    #ft.close()
    fc.close()
