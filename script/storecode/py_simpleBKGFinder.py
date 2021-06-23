#!/usr/bin/env python
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataHist,RooDataSet, RooArgSet, RooArgList
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf

inF=TFile.Open('a.root')

space=RooWorkspace('space',False)

# fit lbtkMass in 2016Data {{{
space.factory('mass[5.100,7.]')
mass=space.var('mass')

inH=inF.Get('lbtkCombBKG')
datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)

# create target PDF.
#space.factory('EXPR::cPDF( "( exp(-1.*(mass-mShift)/(cPar1+cPar2)) - exp(-1.*(mass-mShift)/cPar1) )", mass, mShift[4.8,0.1,10.0], cPar1[0.44,0.001,100.],cPar2[0.0025,0.0000001,10.] )')
space.factory('EXPR::cPDF( "( exp(-1.*(mass-mShift)/(cPar1+cPar2)) - exp(-1.*(mass-mShift)/cPar1) )", mass, mShift[4.8,0.1,10.0], cPar1[0.44,0.001,100.],cPar2[0.0025,0.0000001,10.] )')
myPDF=space.pdf('cPDF')
myPDF.fitTo(datahist)
myPDF.fitTo(datahist)
myPDF.fitTo(datahist)

myFrame=mass.frame()
datahist.plotOn(myFrame)
myPDF.plotOn(myFrame)
canv=TCanvas('c1','c1',1600,1000)
myFrame.Draw()
canv.SaveAs('store_fig/hout_simpleFit_lbDist_from2016Data.png')
canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_from2016Data.C')
# fit lbtkMass in 2016Data end }}}

## fit lbtkMass in Lb MC {{{
##space.factory('lbtkMass[5.1,7.]')
#space.factory('lbtkMass[5.5,5.7]')
#mass=space.var('lbtkMass')
#
#inN=inF.Get('LbTk')
#dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
#
#
## create target PDF.
#space.factory('Gaussian::gPDF_Bd1(lbtkMass,mu1[5.62,4.9,7.0],sigma1[0.01,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd2(lbtkMass,mu2[5.62,4.9,7.0],sigma2[0.05,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd3(lbtkMass,mu3[5.62,4.9,7.0],sigma3[0.05,0.0001,5.])')
##space.factory('SUM::gPDF_Bd(frac1[0.90,0.0001,1.0]*gPDF_Bd1,frac2[0.05,0.0001,1.0]*gPDF_Bd2,gPDF_Bd3)')
#space.factory('SUM::gPDF_Bd(frac1[0.60,0.0001,1.0]*gPDF_Bd1,gPDF_Bd2)')
#myPDF=space.pdf('gPDF_Bd')
#myPDF.fitTo(dataset)
#myPDF.fitTo(dataset)
#myPDF.fitTo(dataset)
#
#myFrame=mass.frame()
#dataset.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromLb.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromLb.C')
## fit lbtkMass in Lb MC end }}}

## fit lbtkMass in antiLb MC {{{
#space.factory('lbtkMass[5.1,7.]')
#mass=space.var('lbtkMass')
#
#inN=inF.Get('AntiLbTk')
#dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
#
#
## create target PDF.
#space.factory('Gaussian::gPDF_Bd1(lbtkMass,mu1[5.50,4.9,7.0],sigma1[0.10,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd2(lbtkMass,mu2[5.80,4.9,7.0],sigma2[0.40,0.0001,5.])')
#space.factory('SUM::gPDF_Bd(frac1[0.34,0.0001,1.0]*gPDF_Bd1,gPDF_Bd2)')
#myPDF=space.pdf('gPDF_Bd')
#myPDF.fitTo(dataset)
#myPDF.fitTo(dataset)
##myPDF.fitTo(dataset)
#
#myFrame=mass.frame()
#dataset.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromAntiLb.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromAntiLb.C')
## fit lbtkMass in antiLb MC end }}}

## fit lbtkMass in BdToJpsiKstar892 MC {{{
##space.factory('lbtkMass[5.5,6.0]')
#space.factory('lbtkMass[5.5,7.0]')
#mass=space.var('lbtkMass')
#
#inH=inF.Get('lbtk_Bd')
#datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
#
#
## create target PDF.
#space.factory('Gaussian::gPDF_Bd1(lbtkMass,mu1[5.73,5.1,7.0],sigma1[0.1,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd2(lbtkMass,mu2[6.44,5.1,7.0],sigma2[0.3,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd3(lbtkMass,mu3[5.99,5.1,7.0],sigma3[0.2,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd4(lbtkMass,mu4[6.50,5.1,7.0],sigma4[0.3,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd5(lbtkMass,mu5[6.70,5.1,7.0],sigma5[0.4,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd6(lbtkMass,mu6[6.90,5.1,7.0],sigma6[0.5,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd7(lbtkMass,mu7[5.40,5.1,7.0],sigma7[0.6,0.0001,5.])')
#gausList=RooArgList(space.pdf('gPDF_Bd1'),space.pdf('gPDF_Bd2'),space.pdf('gPDF_Bd3'),space.pdf('gPDF_Bd4'),space.pdf('gPDF_Bd5'),space.pdf('gPDF_Bd6'),space.pdf('gPDF_Bd7'))
#space.factory('frac1[0.1,0.0001,1.0]')
#space.factory('frac2[0.1,0.0001,1.0]')
#space.factory('frac3[0.1,0.0001,1.0]')
#space.factory('frac4[0.1,0.0001,1.0]')
#space.factory('frac5[0.1,0.0001,1.0]')
#space.factory('frac6[0.05,0.0001,1.0]')
#coefList=RooArgList(space.var('frac1'),space.var('frac2'),space.var('frac3'),space.var('frac4'),space.var('frac5'),space.var('frac6'))
#myPDF=RooAddPdf('gPDF_Bd','gPDF_Bd',gausList,coefList,True)
##
#myPDF=space.pdf('gPDF_Bd')
#myPDF.fitTo(datahist)
#myPDF.fitTo(datahist)
#myPDF.fitTo(datahist)
#
#myFrame=mass.frame()
#datahist.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd4'),RooFit.LineColor(41),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd5'),RooFit.LineColor(42),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd6'),RooFit.LineColor(43),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd7'),RooFit.LineColor(44),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromBd.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromBd.C')
## fit bdMass in BdToJpsiKstar892 MC end }}}

## fit lbtkMass in AntiBdToJpsiKstar892 MC {{{
##space.factory('lbtkMass[5.5,6.0]')
#space.factory('lbtkMass[5.5,7.0]')
#mass=space.var('lbtkMass')
#
#inH=inF.Get('lbtk_AntiBd')
#datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
#
#
## create target PDF.
#space.factory('Gaussian::gPDF_Bd1(lbtkMass,mu1[5.73,5.1,7.0],sigma1[0.1,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd2(lbtkMass,mu2[6.44,5.1,7.0],sigma2[0.3,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd3(lbtkMass,mu3[5.99,5.1,7.0],sigma3[0.2,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd4(lbtkMass,mu4[6.50,5.1,7.0],sigma4[0.3,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd5(lbtkMass,mu5[6.70,5.1,7.0],sigma5[0.4,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd6(lbtkMass,mu6[6.90,5.1,7.0],sigma6[0.5,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd7(lbtkMass,mu7[5.40,5.1,7.0],sigma7[0.6,0.0001,5.])')
#space.factory('SUM::gPDF_Bd(frac1[0.003,0.0001,1.0]*gPDF_Bd1,frac2[0.9,0.0001,1.0]*gPDF_Bd2,frac3[0.2,0.0001,1.0]*gPDF_Bd3,frac4[0.2,0.0001,1.0]*gPDF_Bd4,frac5[0.1,0.0001,1.0]*gPDF_Bd5,frac6[0.05,0.0001,1.0]*gPDF_Bd6,gPDF_Bd7)')
#
#myPDF=space.pdf('gPDF_Bd')
#myPDF.fitTo(datahist)
#myPDF.fitTo(datahist)
#myPDF.fitTo(datahist)
#
#myFrame=mass.frame()
#datahist.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd4'),RooFit.LineColor(41),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd5'),RooFit.LineColor(42),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd6'),RooFit.LineColor(43),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd7'),RooFit.LineColor(44),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromAntiBd.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromAntiBd.C')
## fit bdMass in BdToJpsiKstar892 MC end }}}

## fit lbtkMass in Bs MC {{{
##space.factory('lbtkMass[5.1,7.]')
#space.factory('lbtkMass[5.1,7.]')
#mass=space.var('lbtkMass')
#
#inN=inF.Get('BsToJpsiF')
#dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
#
#
## create target PDF.
#space.factory('EXPR::cPDF( "lbtkMass>mShift?(( exp(-1.*(lbtkMass-mShift)/(cPar1+cPar2)) - exp(-1.*(lbtkMass-mShift)/cPar1) )/cPar2):0.000", lbtkMass, mShift[5.3,0.1,10.0], cPar1[0.05,0.001,100.],cPar2[0.25,0.0000001,50.] )')
#space.factory('Gaussian::gPDF_Bd1(lbtkMass,mu1[5.86,4.9,7.0],sigma1[0.1,0.0001,50.])')
#space.factory('SUM::gPDF_Bd(frac1[0.90,0.0001,1.0]*cPDF,gPDF_Bd1)')
#
#myPDF=space.pdf('gPDF_Bd')
#myPDF.fitTo(dataset)
#myPDF.fitTo(dataset)
#myPDF.fitTo(dataset)
#
#myFrame=mass.frame()
#dataset.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromBs.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromBs.C')
## fit lbtkMass in Lb MC end }}}

# # fit bdMass in BdToJpsiKstar892 MC {{{
# #space.factory('bdMass[4.5,7.]')
# space.factory('bdMass[5.,5.5]')
# mass=space.var('bdMass')
# 
# inH=inF.Get('bd_Bd')
# datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
# 
# 
# # create target PDF.
# space.factory('Gaussian::gPDF_Bd1(bdMass,mu1[5.25,4.9,5.5],sigma1[0.02,0.0001,5.])')
# space.factory('Gaussian::gPDF_Bd2(bdMass,mu2[5.25,4.9,5.5],sigma2[0.01,0.0001,5.])')
# space.factory('Gaussian::gPDF_Bd3(bdMass,mu3[5.25,4.9,5.5],sigma3[0.13,0.0001,5.])')
# space.factory('SUM::gPDF_Bd(frac1[0.34,0.0001,1.0]*gPDF_Bd1,frac2[0.6,0.0001,1.0]*gPDF_Bd2,gPDF_Bd3)')
# myPDF=space.pdf('gPDF_Bd')
# myPDF.fitTo(datahist)
# #myPDF.fitTo(datahist)
# #myPDF.fitTo(datahist)
# 
# myFrame=mass.frame()
# datahist.plotOn(myFrame)
# myPDF.plotOn(myFrame,RooFit.LineColor(2))
# myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
# myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
# myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
# canv=TCanvas('c1','c1',1600,1000)
# canv.Divide(2,1)
# canv.cd(1)
# myFrame.Draw()
# canv.cd(2)
# canv.GetPad(2).SetLogy()
# myFrame.Draw()
# canv.SaveAs('store_fig/hout_simpleFit_bdDist_fromBd.png')
# canv.SaveAs('store_fig/C_hout_simpleFit_bdDist_fromBd.C')
# # fit bdMass in BdToJpsiKstar892 MC end }}}

## fit bdMass in AntiBdToJpsiKstar892 MC {{{
#space.factory('bdMass[4.5,7.]')
#mass=space.var('bdMass')
#
#inH=inF.Get('bd_AntiBd')
#datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
#
## create target PDF.
#space.factory('Gaussian::gPDF_Bd1(bdMass,mu1[5.25,4.9,5.5],sigma1[0.1,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd2(bdMass,mu2[5.30,4.9,5.5],sigma2[1.0,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd3(bdMass,mu3[5.30,4.9,5.5],sigma3[1.0,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd4(bdMass,mu4[5.30,4.9,5.5],sigma4[1.0,0.0001,5.])')
#space.factory('SUM::gPDF_Bd(frac1[0.6,0.0001,1.0]*gPDF_Bd1,frac2[0.2,0.0001,1.0]*gPDF_Bd2,frac3[0.1,0.0001,1.0]*gPDF_Bd3,gPDF_Bd4)')
##space.factory('SUM::gPDF_Bd(frac1[0.6,0.0001,1.0]*gPDF_Bd1,frac2[0.2,0.0001,1.0]*gPDF_Bd2,gPDF_Bd3)')
#myPDF=space.pdf('gPDF_Bd')
#myPDF.fitTo(datahist)
##myPDF.fitTo(datahist)
##myPDF.fitTo(datahist)
#
#myFrame=mass.frame()
#datahist.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd4'),RooFit.LineColor(41),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_bdDist_fromAntiBd.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_bdDist_fromAntiBd.C')
## fit bdMass in BdToJpsiKstar892 MC end }}}

## fit bdMass in Bs MC {{{
##space.factory('bdMass[5.1,7.]')
#space.factory('bdMass[4.5,7.0]')
#mass=space.var('bdMass')
#
#inN=inF.Get('BsToJpsiKK')
#datasets=RooDataSet('datasetO','datasetO',inN,RooArgSet(mass))
#dataset=datasets.reduce(RooFit.Cut('bdMass<5.5'),RooFit.Name('dataset'))
#print 'orig num: {0}, new num: {1}'.format(datasets.sumEntries(),dataset.sumEntries())
#
#getattr(space,'import')(dataset)
#
#
## create target PDF.
#space.factory('KeysPdf::kPDF(bdMass,dataset,NoMirror,1.5)')
#myPDF=space.pdf('kPDF')
#myPDF.fitTo(dataset)
#
#myFrame=mass.frame()
#dataset.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/mytest.png')
##canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromBsKK.C')
## fit bdMass in Bs MC end }}}

## fit bsMass in Bs MC {{{
##space.factory('bsMass[5.1,7.]')
#space.factory('bsMass[5.2,5.5]')
#mass=space.var('bsMass')
#
#inN=inF.Get('BsToJpsiKK')
#dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
#
#
## create target PDF.
#space.factory('Gaussian::gPDF_Bd1(bsMass,mu1[5.36,4.9,7.0],sigma1[0.01,0.0001,5.])')
#space.factory('Gaussian::gPDF_Bd2(bsMass,mu2[5.36,4.9,7.0],sigma2[0.02,0.0001,5.])')
#space.factory('SUM::gPDF_Bd(frac1[0.70,0.0001,1.0]*gPDF_Bd1,gPDF_Bd2)')
#myPDF=space.pdf('gPDF_Bd')
#myPDF.fitTo(dataset)
#myPDF.fitTo(dataset)
#myPDF.fitTo(dataset)
#
#myFrame=mass.frame()
#dataset.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
#myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_bsDist_fromBs.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromBsKK.C')
## fit bsMass in Bs MC end }}}

## fit bsMass in Bd MC {{{
#space.factory('bsMass[5.35,6.0]')
##space.factory('bsMass[4.5,7.]')
#mass=space.var('bsMass')
#
##inN=inF.Get('')
##dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
#inH=inF.Get('bs_Bd')
#datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
#
#
## create target PDF.
#space.factory('EXPR::cPDF( "( exp(-1.*(bsMass-mShift)/(cPar1+cPar2)) - exp(-1.*(bsMass-mShift)/cPar1) )", bsMass, mShift[5.3,0.1,10.0], cPar1[0.05,0.001,100.],cPar2[0.25,0.0000001,50.] )')
#space.factory('Gaussian::gPDF_Bd1(bsMass,mu1[5.86,4.9,7.0],sigma1[0.1,0.0001,50.])')
##space.factory('Gaussian::gPDF_Bd2(bsMass,mu2[5.36,4.9,7.0],sigma2[0.02,0.0001,5.])')
#space.factory('SUM::gPDF_Bd(frac1[0.95,0.0001,1.0]*cPDF,gPDF_Bd1)')
#myPDF=space.pdf('gPDF_Bd')
##myPDF=space.pdf('cPDF')
#myPDF.fitTo(datahist)
#myPDF.fitTo(datahist)
##myPDF.fitTo(datahist)
#
#myFrame=mass.frame()
#datahist.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/hout_simpleFit_bsDist_fromBd.png')
#canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromBd.C')
## fit bsMass in Bd MC end }}}

## fit bsMass in AntiBd MC {{{
#space.factory('bsMass[5.35,6.0]')
##space.factory('bsMass[4.5,7.]')
#mass=space.var('bsMass')
#
##inN=inF.Get('')
##dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
#inH=inF.Get('bs_AntiBd')
#datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
#
#
## create target PDF.
#space.factory('EXPR::cPDF( "( exp(-1.*(bsMass-mShift)/(cPar1+cPar2)) - exp(-1.*(bsMass-mShift)/cPar1) )", bsMass, mShift[5.3,0.1,10.0], cPar1[0.05,0.001,100.],cPar2[0.25,0.0000001,50.] )')
#space.factory('Gaussian::gPDF_Bd1(bsMass,mu1[5.86,4.9,7.0],sigma1[0.1,0.0001,50.])')
##space.factory('Gaussian::gPDF_Bd2(bsMass,mu2[5.36,4.9,7.0],sigma2[0.02,0.0001,5.])')
#space.factory('SUM::gPDF_Bd(frac1[0.95,0.0001,1.0]*cPDF,gPDF_Bd1)')
#myPDF=space.pdf('gPDF_Bd')
##myPDF=space.pdf('cPDF')
#myPDF.fitTo(datahist, RooFit.Minos(True))
#
#myFrame=mass.frame()
#datahist.plotOn(myFrame)
#myPDF.plotOn(myFrame,RooFit.LineColor(2))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd1'),RooFit.LineColor(30),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd2'),RooFit.LineColor(38),RooFit.LineStyle(10))
##myPDF.plotOn(myFrame,RooFit.Components('gPDF_Bd3'),RooFit.LineColor(46),RooFit.LineStyle(10))
#canv=TCanvas('c1','c1',1600,1000)
#canv.Divide(2,1)
#canv.cd(1)
#myFrame.Draw()
#canv.cd(2)
#canv.GetPad(2).SetLogy()
#myFrame.Draw()
#canv.SaveAs('store_fig/aahout_simpleFit_bsDist_fromAntiBd.png')
#canv.SaveAs('store_fig/aaC_hout_simpleFit_bsDist_fromAntiBd.C')
## fit bsMass in Bd MC end }}}
