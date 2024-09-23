#!/usr/bin/env python
# used for MC shape define
# fit MC in LbMass, LbBarMass, BdMass, BdBarMass,BsMass

from array import array
from ROOT import TLegend
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis, TPad, TLine, TGraphErrors, TGraph
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsData, RooKeysPdf

outFileName='store_root/workspace_1stStep_MCShape.root'
outFig='store_fig/pdf_workspace_1stStep_MCShape.pdf'


outFile=TFile(outFileName,'recreate')
figDir=outFile.mkdir('figs')
fitDir=outFile.mkdir('fitRes')

# set output message level
RooMsgService.instance().setGlobalKillBelow(4)

testMode=False
inF=TFile.Open('result_flatNtuple.root')
inFF=TFile.Open('result_flatNtuple_LbTk_preSelection_noKinematicCut.root')

def NewCanvas(name='c1'):
    canv=TCanvas(name,'',1000,1000)
    #canv=TCanvas(name,'',600,550)
    #canv.Divide(2,1)
    #canv.GetPad(2).SetLogy()
    canv.SetFillColor(4000)
    canv.SetFillStyle(4000)
    #canv.GetPad(1).SetFillStyle(4000)
    #canv.GetPad(1).SetFillColor(4000)
    #canv.GetPad(2).SetFillStyle(4000)
    #canv.GetPad(2).SetFillColor(4000)
    return canv
canv=NewCanvas()
canv.SaveAs(outFig+'[')
TGaxis.SetMaxDigits(3)


space=RooWorkspace('space',False)

space.factory('lbtkMass[5.1,8.]')
space.factory('lbtkbarMass[5.1,8.]')
space.factory('bdMass[4.0,7.]')
space.factory('bdbarMass[4.0,7.]')
#space.factory('bsMass[4.5,7.0]')
space.factory('bsMass[5.0,7.5]')
space.factory('tk1Pt[0.,100.]')
space.factory('tk2Pt[0.,100.]')
tk1Pt=space.var('tk1Pt')
tk2Pt=space.var('tk2Pt')


# ########## load workspace ####################
# workspaceFile=TFile.Open('fitResTo2016Data__LbL0.root')
# loadSpace=workspaceFile.Get('space')
# loadSpace.SetName('loadSpace')
# widthMultiPlier=loadSpace.var('data_MC_factor_lbl0Dist_lbl0MC')
# widthMultiPlier.setConstant()
# getattr(space,'import')(widthMultiPlier)

fitToLbMass_2016Data_combinatorialBKG=True
fitToLbMass_LbTkMC=True
fitToLbMass_AntiLbTkMC=True
fitToLbMass_BdK892MC=True
fitToLbMass_AntiBdK892MC=True
fitToLbMass_BsFMC=True

fitToLbBarMass_2016Data_combinatorialBKG=True
fitToLbBarMass_LbTkMC=True
fitToLbBarMass_AntiLbTkMC=True
fitToLbBarMass_BdK892MC=True
fitToLbBarMass_AntiBdK892MC=True
fitToLbBarMass_BsFMC=True

fitToBdMass_LbTkMC=True
fitToBdMass_AntiLbTkMC=True
fitToBdMass_BdK892MC=True
fitToBdMass_AntiBdK892MC=True
fitToBdMass_BsMC=True

fitToBdBarMass_LbTkMC=True
fitToBdBarMass_AntiLbTkMC=True
fitToBdBarMass_BdK892MC=True
fitToBdBarMass_AntiBdK892MC=True
fitToBdBarMass_BsMC=True

fitToBsMass_LbTkMC=True
fitToBsMass_AntiLbTkMC=True
fitToBsMass_BsMC=True
fitToBsMass_BdK892MC=True
fitToBsMass_AntiBdK892MC=True

setAxis=True
xaxisMin=4.0
xaxisMax=7.0


def SetMyRanges(myVar, nErr):
    mean=myVar.getVal()
    errs=myVar.getError()
    myVar.setRange(mean-nErr*errs, mean+nErr*errs)
    return None
def ConstraintVar(space, var):
    space.factory('Gaussian::{0}Constr({0},{1},{2})'.format(var.GetName(),var.getVal(),var.getError()))
    return space.pdf( '{0}.Constr'.format(var.GetName()) )

# fit lbtkMass in 2016Data {{{
if fitToLbMass_2016Data_combinatorialBKG:
    fitLabel='lbtkDist_CMBkg'
    mass=space.var('lbtkMass')
    mass.setRange(fitLabel,5.1,8.0)
    mass.setBins(190)
    bdm=space.var('bdMass')
    bDm=space.var('bdbarMass')
    bsm=space.var('bsMass')

    inF2=TFile.Open('a.root')
    inH=inF2.Get('lbtkCombBKG')
    datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
    # create target PDF.
    space.factory('EXPR::cPDF_{0}( "lbtkMass>mShift_{0}?(( exp(-1.*(lbtkMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(lbtkMass-mShift_{0})/cPar_{0}1) )):0.", lbtkMass, mShift_{0}[4.8,0.1,10.0], cPar_{0}1[0.44,0.001,100.],cPar_{0}2[0.0025,0.0000001,10.] )'.format(fitLabel))
    myPDF=space.pdf('cPDF_{0}'.format(fitLabel))
    fitRes=myPDF.fitTo(datahist,RooFit.Range(fitLabel),RooFit.Save(True))


    myFrame=mass.frame(RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    datahist.plotOn(myFrame)
    myPDF.plotOn(myFrame)

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    inF2.Close()
# fit lbtkMass in 2016Data end }}}

# fit lbtkMass in Lb MC {{{
if fitToLbMass_LbTkMC:
    fitLabel='lbtkDist_lbtkMC'
    mass=space.var('lbtkMass')
    mass.setRange(fitLabel,5.5,5.8)


    inN=inFF.Get('pLbTk/LbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))


    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(lbtkMass,mu_{0}[5.62,4.9,7.0],sigma_MC_{0}1[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(lbtkMass,mu_{0}              ,sigma_MC_{0}2[0.05,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.70,0.6,1.0]*gPDF_MC_{0}1,gPDF_MC_{0}2)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))

    fitRes=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(True),RooFit.Save(True))


    space.var('mu_{0}'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}1'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}2'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}1'.format(fitLabel)).setConstant(True)


    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Range(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_MC_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))


    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    # fit lbtkMass in Lb MC end }}}

    # fit lbtkMass in antiLb MC {{{
if fitToLbMass_AntiLbTkMC:
    fitLabel='lbtkDist_antilbtkMC'
    mass=space.var('lbtkMass')

    inN=inFF.Get('pLbTk/AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(lbtkMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,2.0)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit lbtkMass in antiLb MC end }}}

    # fit lbtkMass in BdToJpsiKstar892 MC {{{
    # bkg : keyspdf
if fitToLbMass_BdK892MC:
    fitLabel='lbtkDist_BdK892MC'
    mass=space.var('lbtkMass')
    mass.setRange(fitLabel,5.5,8.)

    inN=inF.Get('BdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,2.0)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(lbtkMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit lbtkMass in AntiBdToJpsiKstar892 MC {{{
    # recursive AddPdf
if fitToLbMass_AntiBdK892MC:
    fitLabel='lbtkDist_antiBdK892MC'
    mass=space.var('lbtkMass')

    inN=inF.Get('AntiBdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,2.5)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit lbtkMass in BsF MC {{{
    # double-exponential
if fitToLbBarMass_BsFMC:
    fitLabel='lbtkDist_BsFMC'
    mass=space.var('lbtkMass')

    inN=inF.Get('BsToJpsiF')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.8)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(lbtkMass,fitData_{0},NoMirror,1.8)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit lbtkMass in BsF MC end }}}


# fit lbtkbarMass in 2016Data {{{
if fitToLbBarMass_2016Data_combinatorialBKG:
    fitLabel='lbtkbarDist_CMBkg'
    mass=space.var('lbtkbarMass')
    mass.setRange(fitLabel,5.1,8.0)
    mass.setBins(290)
    bdm=space.var('bdMass')
    bDm=space.var('bdbarMass')
    bsm=space.var('bsMass')

    inF2=TFile.Open('a.root')
    inH=inF2.Get('lbtkCombBKG')
    datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
    # create target PDF.
    space.factory('EXPR::cPDF_{0}( "lbtkbarMass>mShift_{0}?(( exp(-1.*(lbtkbarMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(lbtkbarMass-mShift_{0})/cPar_{0}1) )):0.", lbtkbarMass, mShift_{0}[4.8,0.1,10.0], cPar_{0}1[0.44,0.001,100.],cPar_{0}2[0.0025,0.0000001,10.] )'.format(fitLabel))
    myPDF=space.pdf('cPDF_{0}'.format(fitLabel))
    fitRes=myPDF.fitTo(datahist,RooFit.Range(fitLabel),RooFit.Save(True))

    myFrame=mass.frame(RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)');
    datahist.plotOn(myFrame)
    myPDF.plotOn(myFrame)

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    inF2.Close()
    fitDir.cd()
    fitRes.Write(fitLabel)
# fit lbtkbarMass in 2016Data end }}}

# fit lbtkbarMass in Lb MC {{{
if fitToLbBarMass_LbTkMC:
    fitLabel='lbtkbarDist_lbtkMC'
    #space.factory('lbtkbarMass[5.5,5.7]')
    mass=space.var('lbtkbarMass')
    mass.setRange(fitLabel,5.5,5.8)


    inN=inFF.Get('nLbTk/LbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)


    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.7)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(lbtkbarMass,fitData_{0},NoMirror,1.7)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit lbtkbarMass in Lb MC end }}}

    # fit lbtkbarMass in antiLb MC {{{
if fitToLbBarMass_AntiLbTkMC:
    fitLabel='lbtkbarDist_antilbtkMC'
    mass=space.var('lbtkbarMass')
    mass.setRange(fitLabel,5.5,5.8)

    inN=inFF.Get('nLbTk/AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))

    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(lbtkbarMass,mu_{0}[5.62,4.9,7.0],sigma_MC_{0}1[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(lbtkbarMass,mu_{0}              ,sigma_MC_{0}2[0.05,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.70,0.5,1.0]*gPDF_MC_{0}1,gPDF_MC_{0}2)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))

    fitRes=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(True),RooFit.Save(True))


    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Range(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)');
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_MC_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))
    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    # fit lbtkbarMass in antiLb MC end }}}

    # fit lbtkbarMass in BdToJpsiKstar892 MC {{{
    # bkg : keyspdf
if fitToLbBarMass_BdK892MC:
    fitLabel='lbtkbarDist_BdK892MC'
    mass=space.var('lbtkbarMass')
    #mass.setRange(fitLabel,5.5,7.)

    inN=inF.Get('BdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(4000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(40000),RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.9)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0} (lbtkbarMass,fitData_{0},MirrorRight,1.9)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    #myPDF.plotOn(myFrame,RooFit.LineColor(2))
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit lbtkbarMass in AntiBdToJpsiKstar892 MC {{{
    # recursive AddPdf
if fitToLbBarMass_AntiBdK892MC:
    fitLabel='lbtkbarDist_antiBdK892MC'
    mass=space.var('lbtkbarMass')

    inN=inF.Get('AntiBdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(7000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(70000),RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.8)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(lbtkbarMass,fitData_{0},NoMirror,1.8)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit lbtkbarMass in BsF MC {{{
    # double-exponential
if fitToLbBarMass_BsFMC:
    fitLabel='lbtkbarDist_BsFMC'
    mass=space.var('lbtkbarMass')

    inN=inF.Get('BsToJpsiF')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.7)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(lbtkbarMass,fitData_{0},NoMirror,1.7)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit lbtkbarMass in BsF MC end }}}


# fit bdMass in Lb MC {{{
if fitToBdMass_LbTkMC:
    fitLabel='bdDist_lbtkMC'
    #space.factory('bdMass[5.5,5.7]')
    mass=space.var('bdMass')


    inN=inF.Get('LbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdMass<5.6'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,4.0)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,4.0)'.format(fitLabel))


    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdMass in Lb MC end }}}

    # fit bdMass in antiLb MC {{{
if fitToBdMass_AntiLbTkMC:
    fitLabel='bdDist_antilbtkMC'
    mass=space.var('bdMass')

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdMass<5.45'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,3.0)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,3.0)'.format(fitLabel))


    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdMass in antiLb MC end }}}

    # fit bdMass in BdToJpsiKstar892 MC {{{
if fitToBdMass_BdK892MC:
    fitLabel='bdDist_BdK892MC'
    mass=space.var('bdMass')

    inN=inF.Get('BdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))


    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(bdMass,mu_{0}[5.25,4.9,5.5],sigma_MC_{0}1[0.02,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(bdMass,mu_{0}              ,sigma_MC_{0}2[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}3(bdMass,mu_{0}              ,sigma_MC_{0}3[0.13,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.34,0.0001,1.0]*gPDF_MC_{0}1,frac_{0}2[0.6,0.0001,1.0]*gPDF_MC_{0}2,gPDF_MC_{0}3)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))
    fitRes=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(True),RooFit.Save(True))

    myFrame=mass.frame(RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_MC_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit bdMass in AntiBdToJpsiKstar892 MC {{{
if fitToBdMass_AntiBdK892MC:
    fitLabel='bdDist_antiBdK892MC'
    mass=space.var('bdMass')

    inN=inF.Get('AntiBdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.5)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit bdMass in Bs MC {{{
if fitToBdMass_BsMC:
    fitLabel='bdDist_BsFMC'
    mass=space.var('bdMass')

    inN=inF.Get('BsToJpsiF')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdMass<5.5'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,2.0)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bsMass in Bs MC end }}}


# fit bdbarMass in Lb MC {{{
if fitToBdBarMass_LbTkMC:
    fitLabel='bdbarDist_lbtkMC'
    mass=space.var('bdbarMass')
    mass.setRange(fitLabel,5.5,5.8)


    inN=inF.Get('LbTk')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdbarMass<5.40'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},MirrorAsymLeftRight,2.3)'.format(fitLabel))


    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.MirrorAsymLeftRight,2.3)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdbarMass in Lb MC end }}}

    # fit bdbarMass in antiLb MC {{{
if fitToBdBarMass_AntiLbTkMC:
    fitLabel='bdbarDist_antilbtkMC'
    mass=space.var('bdbarMass')

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdbarMass<5.40'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,2.5)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF
    #space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},NoMirror,2.5)'.format(fitLabel))


    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bdbarMass in antiLb MC end }}}

    # fit bdbarMass in BdToJpsiKstar892 MC {{{
if fitToBdBarMass_BdK892MC:
    fitLabel='bdbarDist_BdK892MC'
    mass=space.var('bdbarMass')

    inN=inF.Get('BdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)


    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.5)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    # fit bdbarMass in BdToJpsiKstar892 MC end }}}

    # fit bdbarMass in AntiBdToJpsiKstar892 MC {{{
if fitToBdBarMass_AntiBdK892MC:
    fitLabel='bdbarDist_antiBdK892MC'
    #space.factory('bdbarMass[4.5,7.]')
    mass=space.var('bdbarMass')

    inN=inF.Get('AntiBdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))

    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(bdbarMass,mu_{0}[5.25,4.9,5.5],sigma_MC_{0}1[0.02,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(bdbarMass,mu_{0}              ,sigma_MC_{0}2[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}3(bdbarMass,mu_{0}              ,sigma_MC_{0}3[0.13,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.34,0.0001,1.0]*gPDF_MC_{0}1,frac_{0}2[0.6,0.0001,1.0]*gPDF_MC_{0}2,gPDF_MC_{0}3)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))
    fitRes=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(True),RooFit.Save(True))

    myFrame=mass.frame(RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_MC_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    # fit bdbarMass in BdToJpsiKstar892 MC end }}}

    # fit bdbarMass in Bs MC {{{
if fitToBdBarMass_BsMC:
    fitLabel='bdbarDist_BsFMC'
    mass=space.var('bdbarMass')
    #mass.setRange(fitLabel,5.2,5.5)

    inN=inF.Get('BsToJpsiF')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdbarMass<5.5'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,2.0)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bsMass in Bs MC end }}}


# fit bsMass in Lb MC {{{
if fitToBsMass_LbTkMC:
    fitLabel='bsDist_lbtkMC'
    #space.factory('bsMass[5.5,5.7]')
    mass=space.var('bsMass')


    inN=inF.Get('LbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bsMass<5.6'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,3.0)'.format(fitLabel))


    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,3.0)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bsMass in Lb MC end }}}

    # fit bsMass in antiLb MC {{{
if fitToBsMass_AntiLbTkMC:
    fitLabel='bsDist_antilbtkMC'
    mass=space.var('bsMass')

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bsMass<5.6'))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))


    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.5)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bsMass in antiLb MC end }}}

    # fit bsMass in Bd MC {{{
    # recursive AddPdf
if fitToBsMass_BdK892MC:
    fitLabel='bsDist_BdK892MC'
    mass=space.var('bsMass')

    inN=inF.Get('BdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.5)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    # fit bsMass in Bd MC end }}}

    # fit bsMass in AntiBd MC {{{
    # recursive AddPDF
if fitToBsMass_AntiBdK892MC:
    fitLabel='bsDist_antiBdK892MC'
    mass=space.var('bsMass')

    inN=inF.Get('AntiBdToJpsiKstar892')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
    else:
        dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    #getattr(space,'import')(fitBkg)

    # create target PDF.
    #space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    #myPDF=space.pdf('kPDF_{0}'.format(fitLabel))
    keyPDF=RooKeysPdf('kPDF_{0}'.format(fitLabel),'kPDF_{0}'.format(fitLabel),mass,fitBkg,RooKeysPdf.NoMirror,1.5)
    getattr(space,'import')(keyPDF)


    myPDF=keyPDF

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)

    # fit bsMass in Bd MC end }}}

    # fit bsMass in Bs MC {{{
if fitToBsMass_BsMC:
    fitLabel='bsDist_BsFMC'
    mass=space.var('bsMass')
    mass.setRange(fitLabel,5.25,5.5)

    inN=inF.Get('BsToJpsiF')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))

    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(bsMass,mu_{0}[5.36,4.9,7.0],sigma_MC_{0}1[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(bsMass,mu_{0}              ,sigma_MC_{0}2[0.02,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}3(bsMass,mu_{0}              ,sigma_MC_{0}3[0.04,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.70,0.0001,1.0]*gPDF_MC_{0}1,frac_{0}2[0.25,0.0001,1.0]*gPDF_MC_{0}2,gPDF_MC_{0}3)'.format(fitLabel))
    space.factory('Polynomial::pPDF_MC_{label}(bsMass,{{c1_{label}[0.01,-5.,5.]}})'.format(label=fitLabel)  )
    space.factory('SUM::totPDF_MC_{0}(fracTot_{0}1[0.95,0.0001,1.0]*gPDF_MC_{0},pPDF_MC_{0})'.format(fitLabel))
    myPDF=space.pdf('totPDF_MC_{0}'.format(fitLabel))
    fitRes=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(True),RooFit.Save(True))


    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Range(fitLabel))
    if setAxis: myFrame=mass.frame(xaxisMin,xaxisMax)
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.Name('data'  ),RooFit.LineColor(2))
    myPDF.plotOn(myFrame,RooFit.Name('totFit'),RooFit.LineColor(43),RooFit.LineWidth(1))
    myPDF.plotOn(myFrame,RooFit.Name('sigPDF'),RooFit.LineColor(30),RooFit.Components('gPDF_MC_{0}'.format(fitLabel)))

    myFrame.Draw()
    figDir.cd()
    myFrame.Write(fitLabel)
    canv.SaveAs(outFig)
    fitDir.cd()
    fitRes.Write(fitLabel)
    space.factory('Gaussian::test(bsMass,5.36,0.08)'.format(fitLabel))
    # fit bsMass in Bs MC end }}}
inF.Close()

outFile.cd()
space.Write()
canv.SaveAs(outFig+']')
outFile.Close()
