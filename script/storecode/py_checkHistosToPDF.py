#!/usr/bin/env python

from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataHist, RooArgSet, RooArgList
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace

#fIn=TFile.Open('a.root')
#hist=fIn.Get('bb')
#mass=RooRealVar('mass','mass', 4.8, 6.0)
#rHist=RooDataHist('bindata','bindata', RooArgList(mass),hist)

#subhist=TH1F('sbb','sbb', 170,5.15,6.0)
#for idx in range(170+1):
#    subhist.SetBinContent(idx, hist.GetBinContent(idx+70))
#space=RooWorkspace('w',False)
#space.factory('mass[5.15,6.0]')
#varMass=space.var('mass')
##mass=RooRealVar('mass','mass', 4.8, 6.0)
#rHist=RooDataHist('bindata','bindata', RooArgList(varMass),hist)
#subdatahist=RooDataHist('subdata','subdata', RooArgList(varMass),subhist)
#
#space.factory('Gaussian::Gpdf(mass, Gmean[5.3,4.8,6.0],Gwidth[0.01,0.001,10.])')
#space.factory('Polynomial::Ppdf(mass, {Px1[0.01,-10.,10.],Px2[0.01,-10.,10.],Px3[0.01,-10.,10.]})')
#space.factory('ArgusBG::Apdf(mass, Ax1[-30.,-100.,-0.1],Ax2[5.2,5.0,5.3])')
#space.factory('CBShape::Cpdf(mass, Cmean[90.,60.,120.],Csigma[2.3,1.0,260.],Calpha[-0.1,-5.,0.],Cnum[0.,5.])')
#
#
#totnum=rHist.sumEntries()
#space.factory('SUM::simplemodel(numGAUS[{0},0.,{1}]*Gpdf,numPOLY[{0},0.,{1}]*Ppdf)'.format(totnum/2, totnum))
#space.factory('SUM::myfullmodel(numGAUS[{0},0.,{1}]*Gpdf,numPOLY[{0},0.,{1}]*Ppdf,numARGS[{2},0.,{1}]*Apdf)'.format(totnum/2, totnum, totnum/20))
#
#data=subdatahist
#pdf=space.pdf('simplemodel')
#pdf.fitTo(data)
#
#
#frame=varMass.frame()
#data.plotOn(frame)
#pdf.plotOn(frame)
#
#canv=TCanvas('c1','c1',1600,1000)
#frame.Draw()
#canv.SaveAs('myFit_workspace.png')
#print( 'mynumber : {0} and {1} '.format(space.var('numGAUS').getVal() , space.var('numPOLY').getVal()) )



datasetNames=[
        '2016Data',
        'AntiLbTk',
        'AntiBdToJpsiKstar892',
        'AntiBdToJpsiKstar1432',
        'AntiBdToJpsiKpi',
        'AntiBsToJpsiKK',
       #'AntiBsToJpsiPhi',
        'AntiBsToJpsiF',
        'LbTk',
        'BdToJpsiKstar892',
        'BdToJpsiKstar1432',
        'BdToJpsiKpi',
        'BsToJpsiKK',
       #'BsToJpsiPhi',
        'BsToJpsiF',
        ]
histNames=[
        'lbtkMass',
        'lbtkPt',
        'lbtkbarMass',
        'mumuMass',
        'mumuPt',
        'tktkMass',
        'tktkPt',
        'bsMass',
        'kkMass',
        'bdMass',
        'kpiMass',
        'bdbarMass',
        'kpibarMass',
        ]


fIn=TFile.Open('result_flatNtuple.root')
hDict={ hName : {} for hName in histNames }

for hName in histNames:
    for dName in datasetNames:
        hDict[hName].update( {dName: fIn.Get(dName+"_"+hName)} )
canv=TCanvas('c1','c1',1600,1000)
for hname,hdic in hDict.iteritems():
    canv.Clear()
    canv.Divide(2,1)
    pad1=canv.GetPad(1)
    pad2=canv.GetPad(2)
    pad1.SetLogy(True)
    pad2.SetLogy(False)
    canv.SaveAs('hi.{0}.pdf['.format(hname))
    for nname, hist in hdic.iteritems():
        print nname+"_"+hname
        hist.SetTitle(nname)
        hist.GetXaxis().SetTitle(hname)
        pad1.cd()
        hist.Draw()
        pad2.cd()
        hist.Draw()
        canv.SaveAs('hi.{0}.pdf'.format(hname))
    canv.SaveAs('hi.{0}.pdf]'.format(hname))

