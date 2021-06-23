#!/usr/bin/env python

from array import array
from ROOT import TLegend
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis, TPad, TLine, TGraphErrors, TRatioPlot, TGraph
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsData
def createLegend(plotframe, contentList):
    leg=TLegend(0.60,0.70,0.89,0.89)
    #leg=TLegend(0.70,0.20,0.89,0.59)
    for content in contentList:
        leg.AddEntry(plotframe.findObject(content[0]),content[1],'l')
    leg.SetFillColor(0)
    #leg.SetFillStyle(4000)
    leg.SetBorderSize(0)
    return leg

#TOP_BOTTOM_SEPARATION=0.24
TOP_BOTTOM_SEPARATION=0.30
OVERLAP_MARGIN=0.01
PLOT_X_MIN=0.13
PLOT_Y_MIN=0.105
PLOT_X_MAX=0.95
PLOT_Y_MAX=0.9
def NewTopPad():
    #pad=TPad('toppad','',0.,TOP_BOTTOM_SEPARATION,1.,1.0)
    pad=TPad('toppad','',0.,TOP_BOTTOM_SEPARATION-OVERLAP_MARGIN,1.,1.0)
    pad.SetTicks(1,1)
    pad.SetBottomMargin(0.05)
    pad.SetLeftMargin(PLOT_X_MIN)
    pad.SetRightMargin(1.-PLOT_X_MAX)
    pad.SetTopMargin( (1.-PLOT_Y_MAX)/(1.-TOP_BOTTOM_SEPARATION) )
    #pad.SetBottomMargin( (1.- 0.9)/(1.-0.3) )
    pad.SetFillColor(4000)
    pad.SetFillStyle(4000)
    return pad
def NewBottomPad():
    #pad=TPad('botpad','',0.,0.0,1., TOP_BOTTOM_SEPARATION)
    pad=TPad('botpad','',0.,0.0,1., TOP_BOTTOM_SEPARATION+OVERLAP_MARGIN)
    pad.SetTicks(1,1)
    pad.SetTopMargin(0.025)
    pad.SetLeftMargin(PLOT_X_MIN)
    pad.SetRightMargin(1.-PLOT_X_MAX)
    pad.SetBottomMargin(PLOT_Y_MIN/TOP_BOTTOM_SEPARATION)
    #pad.SetBottomMargin(0.105/0.2)
    pad.SetFillColor(4000)
    pad.SetFillStyle(4000)
    return pad

def GetPullPlotFromFitFrame(xAxis,myFrame):
    pullHist=myFrame.pullHist()
    pullFrame=xAxis.frame(RooFit.Title(''),RooFit.Range(fitLabel))
    pullFrame.addPlotable(pullHist,'pX0') # no error bar
    pullFrame.GetYaxis().SetTitle('#frac{Data-MC}{#sigma_{Data}}')
    pullFrame.SetTitle('')
    pullFrame.SetMinimum(-3.)
    pullFrame.SetMaximum( 3.)

    return pullFrame

def plotInterestingRegionInPull(plotPad):
    print 'hihi'
    print plotPad.GetUxmin()
    print plotPad.GetUxmax()
    print 'hihi'
    x=array('d',[plotPad.GetUxmin(),plotPad.GetUxmax()])
    ex=array('d',[0.,0.])
    y=array('d',[0.,0.])
    ey=array('d',[1.,1.])
    ge=TGraphErrors(2,x,y,ex,ey)
    ge.SetFillColor(7)
    ge.SetFillStyle(3444)
    ge.SetTitle('')
    ge.GetXaxis().SetRangeUser(x[0],x[1])
    ge.GetXaxis().SetLabelOffset(0.015)
    ge.GetXaxis().SetTitle('J/#psi pK^{-} Mass(GeV)')
    ge.GetXaxis().SetTitleSize(0.12)
    ge.GetXaxis().SetLabelSize(0.08)

    ge.GetYaxis().SetRangeUser(-2.,2.)
    ge.GetYaxis().SetTitle('(Data-MC)/#sigma_{Data}')
    ge.GetYaxis().SetTitleSize(0.08)
    ge.GetYaxis().SetTitleOffset(0.5)
    ge.GetYaxis().SetLabelSize(0.08)
    ge.GetYaxis().SetNdivisions(5)

    #ge.SetFillStyle(4020)
    return ge.Clone()

def pullDraw(axis,origPlot, canv):
    pullPlot=GetPullPlotFromFitFrame(axis,origPlot)

    contentPad=NewTopPad()
    binpullPad=NewBottomPad()
    contentPad.Draw()
    binpullPad.Draw()

    canv.cd(1)
    contentPad.cd()
    origPlot.Draw()
    contentPad.Update()
    print 'jjj'
    print contentPad.GetUxmin()
    print contentPad.GetUxmax()
    print 'jjj'

    highLightRegion=plotInterestingRegionInPull(contentPad)
    binpullPad.cd()
    binpullPad.Update()
    highLightRegion.Draw('a3')
    pullPlot.Draw('p same')

# set output message level
RooMsgService.instance().setGlobalKillBelow(4)

testMode=False
allowedNum=5.
inF=TFile.Open('result_flatNtuple.root')

def NewCanvas(name='c1'):
    canv=TCanvas(name,'',700,1000)
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
canv.SaveAs('store_fig/fitResult.pdf[')
TGaxis.SetMaxDigits(3)


space=RooWorkspace('space',False)

space.factory('lbtkMass[5.1,8.]')
space.factory('lbtkbarMass[5.1,8.]')
space.factory('bdMass[4.5,7.]')
space.factory('bdbarMass[4.5,7.]')
#space.factory('bsMass[4.5,7.0]')
space.factory('bsMass[5.1,7.0]')
space.factory('tk1Pt[0.,100.]')
space.factory('tk2Pt[0.,100.]')
tk1Pt=space.var('tk1Pt')
tk2Pt=space.var('tk2Pt')


########## load workspace ####################
workspaceFile=TFile.Open('fitResTo2016Data__LbL0.root')
loadSpace=workspaceFile.Get('space')
loadSpace.SetName('loadSpace')
widthMultiPlier=loadSpace.var('data_MC_factor_lbl0Dist_lbl0MC')
widthMultiPlier.setConstant()
getattr(space,'import')(widthMultiPlier)

# prefit setting {{{
fitToLbMass_2016Data_combinatorialBKG=False
fitToLbMass_LbTkMC=True
fitToLbMass_AntiLbTkMC=False
fitToLbMass_BdK892MC=False
fitToLbMass_AntiBdK892MC=False
fitToLbMass_BsFMC=False

fitToLbBarMass_2016Data_combinatorialBKG=False
fitToLbBarMass_LbTkMC=False
fitToLbBarMass_AntiLbTkMC=False
fitToLbBarMass_BdK892MC=False
fitToLbBarMass_AntiBdK892MC=False
fitToLbBarMass_BsFMC=False

fitToBdMass_LbTkMC=False
fitToBdMass_AntiLbTkMC=False
fitToBdMass_BdK892MC=False
fitToBdMass_AntiBdK892MC=False
fitToBdMass_BsMC=False

fitToBdBarMass_LbTkMC=False
fitToBdBarMass_AntiLbTkMC=False
fitToBdBarMass_BdK892MC=False
fitToBdBarMass_AntiBdK892MC=False
fitToBdBarMass_BsMC=False

fitToBsMass_LbTkMC=False
fitToBsMass_AntiLbTkMC=False
fitToBsMass_BsMC=False
fitToBsMass_BdK892MC=False
fitToBsMass_AntiBdK892MC=False

load2016Data=False

tmpValue=0

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
    mass.setRange(fitLabel,5.1,7.0)
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
    myPDF.fitTo(datahist,RooFit.Range(fitLabel))

    #SetMyRanges(space.var('cPar_{0}1'.format(fitLabel)),5)
    #SetMyRanges(space.var('cPar_{0}2'.format(fitLabel)),5)
    #SetMyRanges(space.var('mShift_{0}'.format(fitLabel)),5)
    ConstraintVar( space, space.var("mShift_{0}".format(fitLabel)) )
    tmpValue=datahist.sumEntries()

    myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)');
    datahist.plotOn(myFrame)
    myPDF.plotOn(myFrame)
    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_from2016Data.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_from2016Data.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    inF2.Close()
# fit lbtkMass in 2016Data end }}}

# fit lbtkMass in Lb MC {{{
if fitToLbMass_LbTkMC:
    fitLabel='lbtkDist_lbtkMC'
    #space.factory('lbtkMass[5.5,5.7]')
    mass=space.var('lbtkMass')
    mass.setRange(fitLabel,5.5,5.8)


    inN=inF.Get('LbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))


    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(lbtkMass,mu_{0}1[5.62,4.9,7.0],sigma_MC_{0}1[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(lbtkMass,mu_{0}2[5.62,4.9,7.0],sigma_MC_{0}2[0.05,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.60,0.0001,1.0]*gPDF_MC_{0}1,gPDF_MC_{0}2)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))

    myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(False))


    space.var('mu_{0}1'.format(fitLabel)).setConstant(True)
    space.var('mu_{0}2'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}1'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}2'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}1'.format(fitLabel)).setConstant(True)

    space.factory('Product::sigma_%s1({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s1})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s2({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s2})' % (fitLabel,fitLabel))
    space.factory('Gaussian::gPDF_{0}1(lbtkMass,mu_{0}1,sigma_{0}1)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}2(lbtkMass,mu_{0}2,sigma_{0}2)'.format(fitLabel))
    space.factory('SUM::gPDF_{0}(frac_{0}1*gPDF_{0}1,gPDF_{0}2)'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Range(fitLabel))
    #myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    myFrame.GetXaxis().SetTitle('')
    myFrame.GetXaxis().SetLabelSize(0)
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))




    #myPDF.plotOn(myFrame,RooFit.Components('gPDF_MC_{0}1'.format(fitLabel)),RooFit.LineColor(30),RooFit.LineStyle(10))
    #myPDF.plotOn(myFrame,RooFit.Components('gPDF_MC_{0}2'.format(fitLabel)),RooFit.LineColor(38),RooFit.LineStyle(10))

    pullFrame=GetPullPlotFromFitFrame(mass,myFrame)

    contentPad=NewTopPad()
    binpullPad=NewBottomPad()
    contentPad.Draw()
    binpullPad.Draw()

    contentPad.cd()
    myFrame.Draw()
    contentPad.Update()
    print ';asdasdf'
    print contentPad.GetUxmin()
    print contentPad.GetUxmax()
    print ';asdasdf'
    binpullPad.cd()

    highLightRegion=plotInterestingRegionInPull(contentPad)
    highLightRegion.Draw('a3')

    pullFrame.Draw('p same')



    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit lbtkMass in Lb MC end }}}

    # fit lbtkMass in antiLb MC {{{
if fitToLbMass_AntiLbTkMC:
    fitLabel='lbtkDist_antilbtkMC'
    mass=space.var('lbtkMass')

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(lbtkMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromAntiLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromAntiLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit lbtkMass in antiLb MC end }}}

    # fit lbtkMass in BdToJpsiKstar892 MC {{{
    # bkg : keyspdf
if fitToLbMass_BdK892MC:
    fitLabel='lbtkDist_BdK892MC'
    mass=space.var('lbtkMass')
    mass.setRange(fitLabel,5.5,7.)

    inN=inF.Get('BdToJpsiKstar892')
    #inN=inF.Get('BdToJpsiKstar1432')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(lbtkMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))



    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit lbtkMass in AntiBdToJpsiKstar892 MC {{{
    # recursive AddPdf
if fitToLbMass_AntiBdK892MC:
    fitLabel='lbtkDist_antiBdK892MC'
    mass=space.var('lbtkMass')

    inN=inF.Get('AntiBdToJpsiKstar892')
    #inN=inF.Get('AntiBdToJpsiKstar1432')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(lbtkMass,fitData_{0},NoMirror,2.5)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromAntiBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromAntiBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
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
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(lbtkMass,fitData_{0},NoMirror,1.8)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromBs.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromBs.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit lbtkMass in BsF MC end }}}


# fit lbtkbarMass in 2016Data {{{
if fitToLbBarMass_2016Data_combinatorialBKG:
    fitLabel='lbtkbarDist_CMBkg'
    mass=space.var('lbtkbarMass')
    mass.setRange(fitLabel,5.1,7.0)
    mass.setBins(190)
    bdm=space.var('bdMass')
    bDm=space.var('bdbarMass')
    bsm=space.var('bsMass')

    inF2=TFile.Open('a.root')
    inH=inF2.Get('lbtkCombBKG')
    datahist=RooDataHist('histogram','histogram',RooArgList(mass),inH)
    # create target PDF.
    space.factory('EXPR::cPDF_{0}( "lbtkbarMass>mShift_{0}?(( exp(-1.*(lbtkbarMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(lbtkbarMass-mShift_{0})/cPar_{0}1) )):0.", lbtkbarMass, mShift_{0}[4.8,0.1,10.0], cPar_{0}1[0.44,0.001,100.],cPar_{0}2[0.0025,0.0000001,10.] )'.format(fitLabel))
    myPDF=space.pdf('cPDF_{0}'.format(fitLabel))
    myPDF.fitTo(datahist,RooFit.Range(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)');
    datahist.plotOn(myFrame)
    myPDF.plotOn(myFrame)
    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbbarDist_from2016Data.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbbarDist_from2016Data.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    inF2.Close()
# fit lbtkbarMass in 2016Data end }}}

# fit lbtkbarMass in Lb MC {{{
if fitToLbBarMass_LbTkMC:
    fitLabel='lbtkbarDist_lbtkMC'
    #space.factory('lbtkbarMass[5.5,5.7]')
    mass=space.var('lbtkbarMass')
    mass.setRange(fitLabel,5.5,5.8)


    inN=inF.Get('LbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    getattr(space,'import')(fitBkg)


    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(lbtkbarMass,fitData_{0},NoMirror,1.7)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbbarDist_fromLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbbarDist_fromLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit lbtkbarMass in Lb MC end }}}

    # fit lbtkbarMass in antiLb MC {{{
if fitToLbBarMass_AntiLbTkMC:
    fitLabel='lbtkbarDist_antilbtkMC'
    mass=space.var('lbtkbarMass')
    mass.setRange(fitLabel,5.5,5.8)

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))

    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(lbtkbarMass,mu_{0}1[5.62,4.9,7.0],sigma_MC_{0}1[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(lbtkbarMass,mu_{0}2[5.62,4.9,7.0],sigma_MC_{0}2[0.05,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.60,0.0001,1.0]*gPDF_MC_{0}1,gPDF_MC_{0}2)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))

    myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(False))

    space.var('mu_{0}1'.format(fitLabel)).setConstant(True)
    space.var('mu_{0}2'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}1'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}2'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}1'.format(fitLabel)).setConstant(True)


    space.factory('Product::sigma_%s1({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s1})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s2({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s2})' % (fitLabel,fitLabel))
    space.factory('Gaussian::gPDF_{0}1(lbtkbarMass,mu_{0}1,sigma_{0}1)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}2(lbtkbarMass,mu_{0}2,sigma_{0}2)'.format(fitLabel))
    space.factory('SUM::gPDF_{0}(frac_{0}1*gPDF_{0}1,gPDF_{0}2)'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Range(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)');
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))
    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbbarDist_fromAntiLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbbarDist_fromAntiLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit lbtkbarMass in antiLb MC end }}}

    # fit lbtkbarMass in BdToJpsiKstar892 MC {{{
    # bkg : keyspdf
if fitToLbBarMass_BdK892MC:
    fitLabel='lbtkbarDist_BdK892MC'
    mass=space.var('lbtkbarMass')
    #mass.setRange(fitLabel,5.5,7.)

    inN=inF.Get('BdToJpsiKstar892')
    #inN=inF.Get('BdToJpsiKstar1432')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(4000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(4000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    else:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(40000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(40000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0} (lbtkbarMass,fitData_{0},MirrorRight,1.9)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    #myPDF.plotOn(myFrame,RooFit.LineColor(2))
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbbarDist_fromBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbbarDist_fromBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit lbtkbarMass in AntiBdToJpsiKstar892 MC {{{
    # recursive AddPdf
if fitToLbBarMass_AntiBdK892MC:
    fitLabel='lbtkbarDist_antiBdK892MC'
    mass=space.var('lbtkbarMass')

    inN=inF.Get('AntiBdToJpsiKstar892')
    #inN=inF.Get('AntiBdToJpsiKstar1432')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(7000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(7000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    else:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(70000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(70000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(lbtkbarMass,fitData_{0},NoMirror,1.8)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbbarDist_fromAntiBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbbarDist_fromAntiBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
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
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(lbtkbarMass,fitData_{0},NoMirror,1.7)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbbarDist_fromBs.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbbarDist_fromBs.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit lbtkbarMass in BsF MC end }}}


# fit bdMass in Lb MC {{{
if fitToBdMass_LbTkMC:
    fitLabel='bdDist_lbtkMC'
    #space.factory('bdMass[5.5,5.7]')
    mass=space.var('bdMass')
    mass.setRange(fitLabel,5.5,5.8)


    inN=inF.Get('LbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdMass<5.6'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,4.0)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdMass in Lb MC end }}}

    # fit bdMass in antiLb MC {{{
if fitToBdMass_AntiLbTkMC:
    fitLabel='bdDist_antilbtkMC'
    mass=space.var('bdMass')

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdMass<5.45'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,3.0)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromAntiLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromAntiLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdMass in antiLb MC end }}}

    # fit bdMass in BdToJpsiKstar892 MC {{{
if fitToBdMass_BdK892MC:
    fitLabel='bdDist_BdK892MC'
    mass=space.var('bdMass')

    #inN=inF.Get('BdToJpsiKstar892')
    inN=inF.Get('BdToJpsiKstar1432')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))


    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(bdMass,mu_{0}1[5.25,4.9,5.5],sigma_MC_{0}1[0.02,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(bdMass,mu_{0}2[5.25,4.9,5.5],sigma_MC_{0}2[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}3(bdMass,mu_{0}3[5.25,4.9,5.5],sigma_MC_{0}3[0.13,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.34,0.0001,1.0]*gPDF_MC_{0}1,frac_{0}2[0.6,0.0001,1.0]*gPDF_MC_{0}2,gPDF_MC_{0}3)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))
    myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(False))
    space.var('mu_{0}1'.format(fitLabel)).setConstant(True)
    space.var('mu_{0}2'.format(fitLabel)).setConstant(True)
    space.var('mu_{0}3'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}1'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}2'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}3'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}1'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}2'.format(fitLabel)).setConstant(True)

    space.factory('Product::sigma_%s1({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s1})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s2({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s2})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s3({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s3})' % (fitLabel,fitLabel))
    space.factory('Gaussian::gPDF_{0}1(bdMass,mu_{0}1,sigma_{0}1)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}2(bdMass,mu_{0}2,sigma_{0}2)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}3(bdMass,mu_{0}3,sigma_{0}3)'.format(fitLabel))
    space.factory('SUM::gPDF_{0}(frac_{0}1*gPDF_{0}1,frac_{0}2*gPDF_{0}2,gPDF_{0}3)'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bdDist_fromBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bdDist_fromBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit bdMass in AntiBdToJpsiKstar892 MC {{{
if fitToBdMass_AntiBdK892MC:
    fitLabel='bdDist_antiBdK892MC'
    #space.factory('bdMass[4.5,7.]')
    mass=space.var('bdMass')

    #inN=inF.Get('AntiBdToJpsiKstar892')
    inN=inF.Get('AntiBdToJpsiKstar1432')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdMass<6.'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bdDist_fromAntiBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bdDist_fromAntiBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdMass in BdToJpsiKstar892 MC end }}}

    # fit bdMass in Bs MC {{{
if fitToBdMass_BsMC:
    fitLabel='bdDist_BsFMC'
    mass=space.var('bdMass')
    #mass.setRange(fitLabel,5.2,5.5)

    inN=inF.Get('BsToJpsiF')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdMass<5.5'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}#pi^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bsDist_fromBs.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromBsKK.C')
    canv.SaveAs('store_fig/fitResult.pdf')
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
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},MirrorAsymLeftRight,2.3)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdbarMass in Lb MC end }}}

    # fit bdbarMass in antiLb MC {{{
if fitToBdBarMass_AntiLbTkMC:
    fitLabel='bdbarDist_antilbtkMC'
    mass=space.var('bdbarMass')

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bdbarMass<5.40'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},NoMirror,2.5)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromAntiLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromAntiLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdbarMass in antiLb MC end }}}

    # fit bdbarMass in BdToJpsiKstar892 MC {{{
if fitToBdBarMass_BdK892MC:
    fitLabel='bdbarDist_BdK892MC'
    mass=space.var('bdbarMass')

    inN=inF.Get('BdToJpsiKstar892')
    #inN=inF.Get('BdToJpsiKstar1432')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(2000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    else:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(20000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(20000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))#,RooFit.Cut('bdbarMass<6.'))
    getattr(space,'import')(fitBkg)


    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))


    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bdbarDist_fromBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bdbarDist_fromBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdbarMass in BdToJpsiKstar892 MC end }}}

    # fit bdbarMass in AntiBdToJpsiKstar892 MC {{{
if fitToBdBarMass_AntiBdK892MC:
    fitLabel='bdbarDist_antiBdK892MC'
    #space.factory('bdbarMass[4.5,7.]')
    mass=space.var('bdbarMass')

    #inN=inF.Get('AntiBdToJpsiKstar892')
    inN=inF.Get('AntiBdToJpsiKstar1432')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))

    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(bdbarMass,mu_{0}1[5.25,4.9,5.5],sigma_MC_{0}1[0.02,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(bdbarMass,mu_{0}2[5.25,4.9,5.5],sigma_MC_{0}2[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}3(bdbarMass,mu_{0}3[5.25,4.9,5.5],sigma_MC_{0}3[0.13,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.34,0.0001,1.0]*gPDF_MC_{0}1,frac_{0}2[0.6,0.0001,1.0]*gPDF_MC_{0}2,gPDF_MC_{0}3)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))
    myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(False))
    space.var('mu_{0}1'.format(fitLabel)).setConstant(True)
    space.var('mu_{0}2'.format(fitLabel)).setConstant(True)
    space.var('mu_{0}3'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}1'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}2'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}3'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}1'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}2'.format(fitLabel)).setConstant(True)

    space.factory('Product::sigma_%s1({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s1})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s2({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s2})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s3({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s3})' % (fitLabel,fitLabel))
    space.factory('Gaussian::gPDF_{0}1(bdbarMass,mu_{0}1,sigma_{0}1)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}2(bdbarMass,mu_{0}2,sigma_{0}2)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}3(bdbarMass,mu_{0}3,sigma_{0}3)'.format(fitLabel))
    space.factory('SUM::gPDF_{0}(frac_{0}1*gPDF_{0}1,frac_{0}2*gPDF_{0}2,gPDF_{0}3)'.format(fitLabel))


    myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bdbarDist_fromAntiBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bdbarDist_fromAntiBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
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
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bdbarMass,fitData_{0},NoMirror,2.0)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{-}#pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bsDist_fromBs.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromBsKK.C')
    canv.SaveAs('store_fig/fitResult.pdf')
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
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,3.0)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bsMass in Lb MC end }}}

    # fit bsMass in antiLb MC {{{
if fitToBsMass_AntiLbTkMC:
    fitLabel='bsDist_antilbtkMC'
    mass=space.var('bsMass')

    inN=inF.Get('AntiLbTk')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bsMass<5.6'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))


    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_lbDist_fromAntiLb.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_lbDist_fromAntiLb.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bsMass in antiLb MC end }}}

    # fit bsMass in Bd MC {{{
    # recursive AddPdf
if fitToBsMass_BdK892MC:
    fitLabel='bsDist_BdK892MC'
    mass=space.var('bsMass')

    #inN=inF.Get('BdToJpsiKstar892')
    inN=inF.Get('BdToJpsiKstar1432')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bsMass>5.1'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))



    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bsDist_fromBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bsMass in Bd MC end }}}

    # fit bsMass in AntiBd MC {{{
    # recursive AddPDF
if fitToBsMass_AntiBdK892MC:
    fitLabel='bsDist_antiBdK892MC'
    mass=space.var('bsMass')

    #inN=inF.Get('AntiBdToJpsiKstar892')
    inN=inF.Get('AntiBdToJpsiKstar1432')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)),RooFit.Cut('bsMass<6.2&&bsMass>5.1'))
    getattr(space,'import')(fitBkg)

    # create target PDF.
    space.factory('KeysPdf::kPDF_{0}(bsMass,fitData_{0},NoMirror,1.5)'.format(fitLabel))
    myPDF=space.pdf('kPDF_{0}'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bsDist_fromAntiBd.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromAntiBd.C')
    canv.SaveAs('store_fig/fitResult.pdf')

    # fit bsMass in Bd MC end }}}

    # fit bsMass in Bs MC {{{
if fitToBsMass_BsMC:
    fitLabel='bsDist_BsFMC'
    mass=space.var('bsMass')
    #mass.setRange(fitLabel,5.2,5.5)

    inN=inF.Get('BsToJpsiF')
    #dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>3.&&tk2Pt>2.')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))

    # create target PDF.
    space.factory('Gaussian::gPDF_MC_{0}1(bsMass,mu_{0}1[5.36,4.9,7.0],sigma_MC_{0}1[0.01,0.0001,5.])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MC_{0}2(bsMass,mu_{0}2[5.36,4.9,7.0],sigma_MC_{0}2[0.02,0.0001,5.])'.format(fitLabel))
    space.factory('SUM::gPDF_MC_{0}(frac_{0}1[0.70,0.0001,1.0]*gPDF_MC_{0}1,gPDF_MC_{0}2)'.format(fitLabel))
    myPDF=space.pdf('gPDF_MC_{0}'.format(fitLabel))
    myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(False))

    space.var('mu_{0}1'.format(fitLabel)).setConstant(True)
    space.var('mu_{0}2'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}1'.format(fitLabel)).setConstant(True)
    space.var('sigma_MC_{0}2'.format(fitLabel)).setConstant(True)
    space.var('frac_{0}1'.format(fitLabel)).setConstant(True)


    space.factory('Product::sigma_%s1({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s1})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s2({data_MC_factor_lbl0Dist_lbl0MC,sigma_MC_%s2})' % (fitLabel,fitLabel))
    space.factory('Gaussian::gPDF_{0}1(bsMass,mu_{0}1,sigma_{0}1)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}2(bsMass,mu_{0}2,sigma_{0}2)'.format(fitLabel))
    space.factory('SUM::gPDF_{0}(frac_{0}1*gPDF_{0}1,gPDF_{0}2)'.format(fitLabel))

    myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi K^{+}K^{-} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2))
    space.pdf('gPDF_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(43),RooFit.LineWidth(1))

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_simpleFit_bsDist_fromBs.eps')
    canv.SaveAs('store_fig/C_hout_simpleFit_bsDist_fromBsKK.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bsMass in Bs MC end }}}
inF.Close()
# prefit setting end }}}

if load2016Data:
    fitToBdfrom2016LoadData=True
    fitTobDfrom2016LoadData=True
    fitToBsfrom2016LoadData=False
    fitToLbfrom2016LoadData=False
    fitTolBfrom2016LoadData=False

    simBdFitData=False
    simLbFitData=False

    veryShortRangeFitLb=True
    veryShortRangeFitlB=False
    inFile16=TFile.Open('result_flatNtuple.root')
    inN16=inFile16.Get('2016Data')

    massLb=space.var('lbtkMass')
    masslB=space.var('lbtkbarMass')
    massBs=space.var('bsMass')
    massBd=space.var('bdMass')
    massbD=space.var('bdbarMass')
    massLb.setRange('sigShortRange',5.3,6.0)
    masslB.setRange('sigShortRange',5.3,6.0)

    massLb.setBins(190)
    masslB.setBins(190)
    massBd.setBins(500)
    massbD.setBins(500)
    massBs.setBins(760)

    loadDatasetLb=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massLb,tk1Pt,tk2Pt))
    loadDatasetlB=RooDataSet('loadData16','loadData16',inN16,RooArgSet(masslB,tk1Pt,tk2Pt))
    loadDatasetBs=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massBs,tk1Pt,tk2Pt))
    loadDatasetBd=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massBd,tk1Pt,tk2Pt))
    loadDatasetbD=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massbD,tk1Pt,tk2Pt))
    totNum=inN16.GetEntries()
    space.factory('numLb[{0},0.,{1}]'.format(2000,totNum))
    space.factory('numlB[{1},0.,{1}]'.format(2000,totNum))
    space.factory('numBs[{0},0.,{1}]'.format(totNum/4,totNum))
    space.factory('numBd[{0},0.,{1}]'.format(totNum/3,totNum))
    space.factory('numbD[{0},0.,{1}]'.format(totNum/3,totNum))

    if not testMode:
        outfile=TFile('fitResTo2016Data.root','recreate')


    # fit 2016 data in Bd mass window {{{
    if fitToBdfrom2016LoadData:
        massBd.setRange('sigRange',5.0,6.0)

        label='BdBKG'
        space.factory('Gaussian::gau_{0}1(bdMass,mu_{0}1[4.83,3.0,8.0],sig_{0}1[0.133,0.001,10.0])'.format(label))
        space.factory('Gaussian::gau_{0}2(bdMass,mu_{0}2[5.43,3.0,8.0],sig_{0}2[0.865,0.001,10.0])'.format(label))
        space.factory('Gaussian::gau_{0}3(bdMass,mu_{0}3[6.65,3.0,8.0],sig_{0}3[0.175,0.001,10.0])'.format(label))
        space.factory('Gaussian::gau_{0}4(bdMass,mu_{0}4[4.61,3.0,8.0],sig_{0}4[0.094,0.001,10.0])'.format(label))
        space.factory('Gaussian::gau_{0}5(bdMass,mu_{0}4[4.61,3.0,8.0],sig_{0}4[0.094,0.001,10.0])'.format(label))
        space.factory('gbkgfrac_{0}1[0.8029,0.0001,1.0]'.format(label))
        space.factory('gbkgfrac_{0}2[0.9965,0.0001,1.0]'.format(label))
        space.factory('gbkgfrac_{0}3[0.0805,0.0001,1.0]'.format(label))
        space.factory('gbkgfrac_{0}4[0.1805,0.0001,1.0]'.format(label))

        gBKG=RooAddPdf('gBKGs_{0}'.format(label),'gBKGs_{0}'.format(label),
                RooArgList( space.pdf('gau_{0}1'.format(label)),
                            space.pdf('gau_{0}2'.format(label)),
                            space.pdf('gau_{0}3'.format(label)),
                            space.pdf('gau_{0}4'.format(label)), ),
                RooArgList( space.var('gbkgfrac_{0}1'.format(label)),
                            space.var('gbkgfrac_{0}2'.format(label)),
                            space.var('gbkgfrac_{0}3'.format(label)), ),
                True)
        getattr(space,'import')(gBKG)

        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/2,totNum))
        myPDF=RooAddPdf('totBdDist','totBdDist',
                RooArgList( space.pdf('gBKGs_{0}'.format(label)),
                            space.pdf('gPDF_bdDist_BdK892MC'),
                            space.pdf('kPDF_bdDist_antiBdK892MC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD') ),
                False)
        getattr(space,'import')(myPDF)

        binData=loadDatasetBd.reduce('tk1Pt>3.&&tk2Pt>2.').binnedClone('binBd')
        if not testMode:
            fitres=myPDF.fitTo(binData,RooFit.Range('sigRange'),RooFit.Save())
            var=space.var('numBd')
            #N=var.getVal()
            #E=var.getError()
            #var.setRange(N-allowedNum*E,N+allowedNum*E)
            space.factory('Gaussian::numBdConstr(numBd,{0},{1})'.format(var.getVal(),var.getError()))


        plotframe=massBd.frame(RooFit.Title(label),RooFit.Range('sigRange'))
        binData.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_bdDist_BdK892MC'       .format(label)),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bdDist_antiBdK892MC'   .format(label)),RooFit.LineStyle(10),RooFit.LineColor(38))

        plotframe.GetXaxis().SetTitle('J/#psi K^{+} #pi^{-} Mass(GeV)')
        canv.cd(1)
        plotframe.Draw()
        canv.cd(2)
        plotframe.Draw()
        canv.SaveAs('store_fig/hout_dataFit_BdDist.eps')
        canv.SaveAs('store_fig/C_hout_dataFit_BdDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')

        if not testMode:
            fitres.Write(label)
    # fit 2016 data in Bd mass window end }}}
    # fit 2016 data in BdBar mass window {{{
    if fitTobDfrom2016LoadData:
        massbD.setRange('sigRange',5.0,6.0)
        massbD.setRange('showRange',5.1,5.4)

        label='bDBKG'
        space.factory('Gaussian::gau_{0}1(bdbarMass,mu_{0}1[4.83,3.0,8.0],sig_{0}1[0.242,0.001,10.0])'.format(label))
        space.factory('Gaussian::gau_{0}2(bdbarMass,mu_{0}2[5.56,3.0,8.0],sig_{0}2[0.563,0.001,10.0])'.format(label))
        space.factory('Gaussian::gau_{0}3(bdbarMass,mu_{0}3[5.52,3.0,8.0],sig_{0}3[0.095,0.001,10.0])'.format(label))
        space.factory('Gaussian::gau_{0}4(bdbarMass,mu_{0}4[4.68,3.0,8.0],sig_{0}4[0.065,0.001,10.0])'.format(label))
        space.factory('gbkgfrac_{0}1[0.737,0.0001,1.0]'.format(label)),
        space.factory('gbkgfrac_{0}2[0.664,0.0001,1.0]'.format(label)),
        space.factory('gbkgfrac_{0}3[0.102,0.0001,1.0]'.format(label)),

        gBKG=RooAddPdf('gBKGs_{0}'.format(label),'gBKGs_{0}'.format(label),
                RooArgList( space.pdf('gau_{0}1'.format(label)),
                            space.pdf('gau_{0}2'.format(label)),
                            space.pdf('gau_{0}3'.format(label)),
                            space.pdf('gau_{0}4'.format(label)), ),
                RooArgList( space.var('gbkgfrac_{0}1'.format(label)),
                            space.var('gbkgfrac_{0}2'.format(label)),
                            space.var('gbkgfrac_{0}3'.format(label)), ),
                True)
        getattr(space,'import')(gBKG)

        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/2,totNum))
        myPDF=RooAddPdf('totbDDist','totbDDist',
                RooArgList( space.pdf('gBKGs_{0}'.format(label)),
                            space.pdf('kPDF_bdbarDist_BdK892MC'),
                            space.pdf('gPDF_bdbarDist_antiBdK892MC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD') ),
                False)
        getattr(space,'import')(myPDF)

        binData=loadDatasetbD.reduce('tk1Pt>3.&&tk2Pt>2.').binnedClone('binbD')
        if not testMode:
            fitres=myPDF.fitTo(binData,RooFit.Range('sigRange'),RooFit.Save(),RooFit.ExternalConstraints(RooArgSet(space.pdf('numBdConstr'))))
            var=space.var('numbD')
            #N=var.getVal()
            #E=var.getError()
            #var.setRange(N-allowedNum*E,N+allowedNum*E)
            space.factory('Gaussian::numbDConstr(numbD,{0},{1})'.format(var.getVal(),var.getError()))


        plotframe=massbD.frame(RooFit.Title(label),RooFit.Range('sigRange'),RooFit.Bins(500))

        binData.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bdbarDist_BdK892MC'       .format(label)),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_bdbarDist_antiBdK892MC'   .format(label)),RooFit.LineStyle(10),RooFit.LineColor(38))

        plotframe.GetXaxis().SetTitle('J/#psi #pi^{+} K^{-} Mass(GeV)')
        canv.cd(1)
        plotframe.Draw()
        canv.cd(2)
        plotframe.Draw()
        canv.SaveAs('store_fig/hout_dataFit_bDDist.eps')
        canv.SaveAs('store_fig/C_hout_dataFit_bDDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')


        if not testMode:
            fitres.Write(label)
    # fit 2016 data in Bd mass window end }}}

    # fit 2016 data in Bs mass window {{{
    if fitToBsfrom2016LoadData:
        massBs.setRange('sigRange',5.1,7.0)

        label='BsBKG'
        space.factory('Gaussian::gau_{0}1(bsMass,mu_{0}1[4.92,4.5,6.0],sig_{0}1[0.212,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}2(bsMass,mu_{0}2[5.31,4.5,6.0],sig_{0}2[0.630,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}3(bsMass,mu_{0}3[4.85,4.5,6.0],sig_{0}3[0.059,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}4(bsMass,mu_{0}4[5.00,4.5,6.0],sig_{0}4[0.100,0.001,5.0])'.format(label))
        #space.factory('SUM::gBKGs_{1}({0}frac_{1}1[0.346,0.0001,1.0]*gau_{1}1,{0}frac_{1}2[0.529,0.0001,1.0]*gau_{1}2,gau_{1}3)'.format('gbkg',label))
        space.factory('SUM::gBKGs_{1}({0}frac_{1}1[0.346,0.0001,1.0]*gau_{1}1,{0}frac_{1}2[0.400,0.0001,1.0]*gau_{1}2,{0}frac_{1}3[0.100,0.0001,1.0]*gau_{1}3,gau_{1}4)'.format('gbkg',label))

        totNum=loadDatasetBs.sumEntries()
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/10,totNum))
        myPDF=RooAddPdf('totBsDist','totBsDist',
                RooArgList( space.pdf('gBKGs_{0}'.format(label)),
                            space.pdf('kPDF_bsDist_BdK892MC'),
                            space.pdf('kPDF_bsDist_antiBdK892MC'),
                            space.pdf('gPDF_bsDist_BsFMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD'),
                            space.var('numBs') ),
                False)
        getattr(space,'import')(myPDF)



        if not testMode:
            fitres=myPDF.fitTo(loadDatasetBs.binnedClone('binBs'),RooFit.Save(),RooFit.Range('sigRange'))


        plotframe=massBs.frame(RooFit.Title(label),RooFit.Range('sigRange'))
        loadDatasetBs.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))

        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_BdK892MC'       .format(label)),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_antiBdK892MC'   .format(label)),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_bsDist_BsFMC'          .format(label)),RooFit.LineStyle(3 ),RooFit.LineColor(2 ))
        #myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_lbtkMC'         .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(41))
        #myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_antilbtkMC'     .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(46))

        plotframe.GetXaxis().SetTitle('J/#psi K^{+} K^{-} Mass(GeV)')
        canv.cd(1)
        plotframe.Draw()
        canv.cd(2)
        plotframe.Draw()
        canv.SaveAs('store_fig/hout_dataFit_bsDist.eps')
        canv.SaveAs('store_fig/C_hout_dataFit_bsDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')

        if not testMode:
            fitres.Write(label)
    # fit 2016 data in Bs mass window end }}}}

    # fit 2016 data in Lb mass window {{{
    if fitToLbfrom2016LoadData:
        massLb.setRange('sigRange',5.45,7.0)

        label='LbSig'
        space.factory('Gaussian::gau_{0}1(lbtkMass,mu_{0}1[4.86,4.5,6.0],sig_{0}1[0.212,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}2(lbtkMass,mu_{0}2[5.37,4.5,6.0],sig_{0}2[0.630,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}3(lbtkMass,mu_{0}3[5.49,4.5,6.0],sig_{0}3[0.059,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}4(lbtkMass,mu_{0}4[5.00,4.5,6.0],sig_{0}4[0.100,0.001,5.0])'.format(label))
        space.factory('SUM::gBKGs_{1}({0}frac_{1}1[0.132,0.0001,1.0]*gau_{1}1,{0}frac_{1}2[0.109,0.0001,1.0]*gau_{1}2,gau_{1}3)'.format('gbkg',label))

        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/2,totNum))
        myPDF=RooAddPdf('totLbDist','totLbDist',
                RooArgList( space.pdf('cPDF_lbtkDist_CMBkg'),
                #RooArgList( space.pdf('gBKGs_{0}'.format(label)),
                            space.pdf('kPDF_lbtkDist_BdK892MC'),
                            space.pdf('kPDF_lbtkDist_antiBdK892MC'),
                            space.pdf('kPDF_lbtkDist_BsFMC'),
                            space.pdf('gPDF_lbtkDist_lbtkMC'),
                            space.pdf('kPDF_lbtkDist_antilbtkMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD'),
                            space.var('numBs'),
                            space.var('numLb'),
                            space.var('numLb') ),
                           #space.var('numlB') ),
                False)
        getattr(space,'import')(myPDF)

        binData=loadDatasetLb.binnedClone('binLb')
        if not testMode:
            pass
        fitres=myPDF.fitTo(binData,RooFit.Range('sigRange'),RooFit.Save(),RooFit.Minos(True))


        plotframe=massLb.frame(RooFit.Title(label),RooFit.Range('sigRange'))
        print tmpValue
        tmpPlotContent=space.pdf('cPDF_lbtkDist_CMBkg').generate(RooArgSet(massLb),int(tmpValue))

        binData.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkDist_BdK892MC'       .format(label)),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkDist_antiBdK892MC'   .format(label)),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkDist_BsFMC'          .format(label)),RooFit.LineStyle(3 ),RooFit.LineColor(2 ))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_lbtkDist_lbtkMC'         .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkDist_antilbtkMC'     .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(46))
        #tmpPlotContent.plotOn(plotframe,RooFit.LineColor(2),RooFit.MarkerColor(2))
        myPDF.plotOn(plotframe,RooFit.Components('cPDF_lbtkDist_CMBkg'),RooFit.LineStyle(1),RooFit.LineColor(30))

        plotframe.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
        canv.cd(1)
        plotframe.Draw()
        canv.cd(2)
        plotframe.Draw()
        canv.SaveAs('store_fig/hout_dataFit_lbDist.eps')
        canv.SaveAs('store_fig/C_hout_dataFit_lbDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')

        if not testMode:
            fitres.Write(label)
    # fit 2016 data in Lb mass window end }}}
    # fit 2016 data in lB mass window {{{
    if fitTolBfrom2016LoadData:
        masslB.setRange('sigRange',5.1,7.0)

        label='lBSig'
        space.factory('Gaussian::gau_{0}1(lbtkbarMass,mu_{0}1[4.86,4.5,6.0],sig_{0}1[0.212,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}2(lbtkbarMass,mu_{0}2[5.37,4.5,6.0],sig_{0}2[0.630,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}3(lbtkbarMass,mu_{0}3[5.49,4.5,6.0],sig_{0}3[0.059,0.001,5.0])'.format(label))
        space.factory('Gaussian::gau_{0}4(lbtkbarMass,mu_{0}4[5.00,4.5,6.0],sig_{0}4[0.100,0.001,5.0])'.format(label))
        space.factory('SUM::gBKGs_{1}({0}frac_{1}1[0.132,0.0001,1.0]*gau_{1}1,{0}frac_{1}2[0.109,0.0001,1.0]*gau_{1}2,gau_{1}3)'.format('gbkg',label))

        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/2,totNum))
        myPDF=RooAddPdf('totlBDist','totlBDist',
                RooArgList( space.pdf('cPDF_lbtkbarDist_CMBkg'),
                            space.pdf('kPDF_lbtkbarDist_BdK892MC'),
                            space.pdf('kPDF_lbtkbarDist_antiBdK892MC'),
                            space.pdf('kPDF_lbtkbarDist_BsFMC'),
                            space.pdf('kPDF_lbtkbarDist_lbtkMC'),
                            space.pdf('gPDF_lbtkbarDist_antilbtkMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD'),
                            space.var('numBs'),
                            space.var('numLb'),
                            space.var('numlB') ),
                False)
        getattr(space,'import')(myPDF)

        binData=loadDatasetlB.binnedClone('binlB')
        if not testMode:
            fitres=myPDF.fitTo(binData,RooFit.Range('sigRange'),RooFit.Save(),RooFit.Minos(True))


        plotframe=masslB.frame(RooFit.Title(label))
        binData.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkbarDist_BdK892MC'       .format(label)),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkbarDist_antiBdK892MC'   .format(label)),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkbarDist_BsFMC'          .format(label)),RooFit.LineStyle(3 ),RooFit.LineColor(2 ))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_lbtkbarDist_lbtkMC'         .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_lbtkbarDist_antilbtkMC'     .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(46))

        plotframe.GetXaxis().SetTitle('J/#psi K^{+} #bar{p} Mass(GeV)')
        canv.cd(1)
        plotframe.Draw()
        canv.cd(2)
        plotframe.Draw()
        canv.SaveAs('store_fig/hout_dataFit_lBDist.eps')
        canv.SaveAs('store_fig/C_hout_dataFit_lBDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')

        if not testMode:
            fitres.Write(label)
    # fit 2016 data in lB mass window end }}}



    # simultaneous fit to bd {{{
    if simBdFitData:
        #if not fitToBdfrom2016LoadData or fitToBsfrom2016LoadData or fitToLbfrom2016LoadData:
        if False:
            print '----- ERROR ---- parameters not enough!!!!'
            exit()
        pass
        label='simulBdFit'
        space.factory('BdCat[BdFit,bDFit]')
        space.factory('SIMUL:simulBdFit(BdCat,BdFit=totBdDist,bDFit=totbDDist)')
        theCategory=space.cat('BdCat')
        simulFit=space.pdf('simulBdFit')

        totalData=RooDataSet(
                'combData','combData',
                RooArgSet(massBd,massbD),RooFit.Index(theCategory),
                RooFit.Import('BdFit',loadDatasetBd.reduce(RooArgSet(massBd))),
                RooFit.Import('bDFit',loadDatasetbD.reduce(RooArgSet(massbD)))
                )

        if not testMode:
            fitres=simulFit.fitTo(totalData.binnedClone('combBinDataFor{0}'.format(label)),RooFit.Save(),RooFit.Minos(True))

        plotframe1=massBd.frame(RooFit.Title("Bd mass window in 2016 data")    )
        totalData.plotOn(plotframe1,RooFit.Cut('BdCat==BdCat::BdFit'))
        simulFit.plotOn(plotframe1,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'BdFit'),RooFit.LineWidth(1),RooFit.LineColor(2))
        simulFit.plotOn(plotframe1,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'BdFit'),RooFit.LineStyle(10),RooFit.LineColor(41),RooFit.Components('gPDF_bdDist_BdK892MC'))
        simulFit.plotOn(plotframe1,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'BdFit'),RooFit.LineStyle(10),RooFit.LineColor(46),RooFit.Components('kPDF_bdDist_antiBdK892MC'))

        plotframe2=massbD.frame(RooFit.Title("Bd bar mass window in 2016 data"))
        totalData.plotOn(plotframe2,RooFit.Cut('BdCat==BdCat::bDFit'))
        simulFit.plotOn(plotframe2,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'bDFit'),RooFit.LineWidth(1),RooFit.LineColor(2))
        simulFit.plotOn(plotframe2,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'bDFit'),RooFit.LineStyle(10),RooFit.LineColor(41),RooFit.Components('kPDF_bdbarDist_BdK892MC'))
        simulFit.plotOn(plotframe2,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'bDFit'),RooFit.LineStyle(10),RooFit.LineColor(46),RooFit.Components('gPDF_bdbarDist_antiBdK892MC'))

        canv.GetPad(1).SetLogy(False)
        canv.GetPad(2).SetLogy(False)
        plotframe1.GetXaxis().SetTitle('J/#psi K^{+} #pi^{-} Mass(GeV)')
        plotframe2.GetXaxis().SetTitle('J/#psi #pi^{+} K^{-} Mass(GeV)')
        canv.cd(1)
        plotframe1.Draw()
        canv.cd(2)
        plotframe2.Draw()
        canv.SaveAs('store_fig/hout_simuldataFit_BdDist.eps')
        canv.SaveAs('store_fig/C_hout_sumuldataFit_BdDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')


        if not testMode:
            fitres.Write(label)
    # simultaneous fit end }}}

    # simultaneous fit to Lb {{{
    if simLbFitData:
        #if not fitToBdfrom2016LoadData or fitToBsfrom2016LoadData or fitToLbfrom2016LoadData:
        if False:
            print '----- ERROR ---- parameters not enough!!!!'
            exit()
        pass
        label='simulLbFit'
        space.factory('LbCat[LbFit,lBFit]')
        space.factory('SIMUL:simulLbFit(LbCat,LbFit=totLbDist,lBFit=totlBDist)')
        theCategory=space.cat('LbCat')
        simulFit=space.pdf('simulLbFit')

        totalData=RooDataSet(
                'combData','combData',
                RooArgSet(massLb,masslB),RooFit.Index(theCategory),
                RooFit.Import('LbFit',loadDatasetLb.reduce(RooArgSet(massLb))),
                RooFit.Import('lBFit',loadDatasetlB.reduce(RooArgSet(masslB)))
                )

        if not testMode:
            fitres=simulFit.fitTo(totalData.binnedClone('combBinDataFor{0}'.format(label)),RooFit.Save())

        plotframe1=massLb.frame(RooFit.Title("Lb mass window in 2016 data")    ,RooFit.Range('sigRange'))
        totalData.plotOn(plotframe1,RooFit.Cut('LbCat==LbCat::LbFit'))
        simulFit.plotOn(plotframe1,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'LbFit'),RooFit.LineWidth(1),RooFit.LineColor(2))
        simulFit.plotOn(plotframe1,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'LbFit'),RooFit.LineStyle(10),RooFit.LineColor(41),RooFit.Components('gPDF_lbtkDist_lbtkMC'))
        simulFit.plotOn(plotframe1,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'LbFit'),RooFit.LineStyle(10),RooFit.LineColor(46),RooFit.Components('kPDF_lbtkDist_antilbtkMC'))

        plotframe2=masslB.frame(RooFit.Title("Lb bar mass window in 2016 data"),RooFit.Range('sigRange'))
        totalData.plotOn(plotframe2,RooFit.Cut('LbCat==LbCat::lBFit'))
        simulFit.plotOn(plotframe1,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'lBFit'),RooFit.LineWidth(1),RooFit.LineColor(2))
        simulFit.plotOn(plotframe2,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'lBFit'),RooFit.LineStyle(10),RooFit.LineColor(41),RooFit.Components('kPDF_lbtkbarDist_lbtkMC'))
        simulFit.plotOn(plotframe2,RooFit.ProjWData(totalData),RooFit.Slice(theCategory,'lBFit'),RooFit.LineStyle(10),RooFit.LineColor(46),RooFit.Components('gPDF_lbtkbarDist_antilbtkMC'))

        canv.GetPad(1).SetLogy(False)
        canv.GetPad(2).SetLogy(False)
        plotframe1.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
        plotframe2.GetXaxis().SetTitle('J/#psi K^{+} #bar{p} Mass(GeV)')
        canv.cd(1)
        plotframe1.Draw()
        canv.cd(2)
        plotframe2.Draw()
        canv.SaveAs('store_fig/hout_simuldataFit_LbDist.eps')
        canv.SaveAs('store_fig/C_hout_sumuldataFit_LbDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')


        if not testMode:
            fitres.Write(label)
    # simultaneous fit end }}}

    canv.Clear()
    canv.SetFillColor(4000)
    canv.SetFillStyle(4000)
    canv.cd()

    # fit 2016 data in short range Lb mass window {{{
    if veryShortRangeFitLb:

        label='ShortRangeLbFit'
        #space.factory('Polynomial::pPDF_{0}'.format(label)+'(lbtkMass,{c1[0.01,-5.,5.],c2[0.01,-5.,5.]})')
        #space.factory('Exponential::ePDF_{0}'.format(label)+'(lbtkMass,c1[0.2,-10.,1.])')
        space.factory('EXPR::cPDF_{0}( "lbtkMass>mShift_{0}?(( exp(-1.*(lbtkMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(lbtkMass-mShift_{0})/cPar_{0}1) )):0.", lbtkMass, mShift_{0}[4.8,4.0,5.2], cPar_{0}1[0.44,0.001,100.],cPar_{0}2[0.0025,0.0000001,10.] )'.format(label))
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label, totNum,totNum))
        myPDF=RooAddPdf('smallLbDist','smallLbDist',
                #RooArgList( space.pdf('pPDF_{0}'.format(label)),
                #RooArgList( space.pdf('ePDF_{0}'.format(label)),
                RooArgList( space.pdf('cPDF_{0}'.format(label)),
                            space.pdf('kPDF_lbtkDist_BdK892MC'),
                            space.pdf('kPDF_lbtkDist_antiBdK892MC'),
                            space.pdf('gPDF_lbtkDist_lbtkMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD'),
                            space.var('numLb') ),
                False)
        getattr(space,'import')(myPDF)

        binData=loadDatasetLb.reduce('tk1Pt>3.&&tk2Pt>2.').binnedClone('shortBinLb')

        fitres=myPDF.fitTo(binData,RooFit.Range('sigShortRange'),RooFit.Save(),RooFit.Minos(False),
                #RooFit.ExternalConstraints( RooArgSet(space.pdf('numbDConstr'),space.pdf('numBdConstr')) )
                    )

        plotframe=massLb.frame(RooFit.Title(label),RooFit.Range('sigShortRange'))
        binData.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        #myPDF.plotOn(plotframe,RooFit.Name('combBkg_{0}'.format(label)),RooFit.Components('pPDF_{0}'                     .format(label)),RooFit.LineStyle(1) ,RooFit.LineColor(41))
        #myPDF.plotOn(plotframe,RooFit.Name('combBkg_{0}'.format(label)),RooFit.Components('ePDF_{0}'                     .format(label)),RooFit.LineStyle(1) ,RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Name('combBkg_{0}'.format(label)),RooFit.Components('cPDF_{0}'                     .format(label)),RooFit.LineStyle(1) ,RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Name('BdBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_BdK892MC'                     ),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Name('bDBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_antiBdK892MC'                 ),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Name('LbSig_{0}'.format(label))  ,RooFit.Components('gPDF_lbtkDist_lbtkMC'                       ),RooFit.LineStyle(5 ),RooFit.LineColor(2) )

        plotframe.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
        plotframe.SetMaximum( 1.2*plotframe.GetMaximum() )
        plotframe.Draw()
        plotContent=[
            ['combBkg_{0}'.format(label) ,'combinatorial background',],
            ['BdBkg_{0}'.format(label)   ,'B^{0}_{d} candidate',],
            ['bDBkg_{0}'.format(label)   ,'#bar{B^{0}_{d}} candidate',],
            ['LbSig_{0}'.format(label)   ,'#Lambda^{0}_{b} candidate',],
            ]
        leg=createLegend(plotframe,plotContent)
        leg.Draw('same')


        canv.SaveAs('store_fig/hout_shortRangeDataFit_lbDist.eps')
        canv.SaveAs('store_fig/C_hout_shortRangeDataFit_lbDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')

        if not testMode:
            fitres.Write(label)
    # fit 2016 data in Lb mass window end }}}
    # fit 2016 data in short range lB mass window {{{
    if veryShortRangeFitlB:

        label='ShortRangelBFit'
        space.factory('Polynomial::pPDF_{0}'.format(label)+'(lbtkbarMass,{c1[0.01,-5.,5.],c2[0.01,-5.,5.]})')
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label, totNum,totNum))
        myPDF=RooAddPdf('smalllBDist','smalllBDist',
                RooArgList( space.pdf('pPDF_{0}'.format(label)),
                            space.pdf('kPDF_lbtkbarDist_BdK892MC'),
                            space.pdf('kPDF_lbtkbarDist_antiBdK892MC'),
                            space.pdf('gPDF_lbtkbarDist_antilbtkMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD'),
                            space.var('numlB') ),
                False)
        getattr(space,'import')(myPDF)

        binData=loadDatasetlB.binnedClone('shortBinlB')

        fitres=myPDF.fitTo(binData,RooFit.Range('sigShortRange'),RooFit.Save(),RooFit.Minos(False),
                RooFit.ExternalConstraints( RooArgSet(space.pdf('numbDConstr'),space.pdf('numBdConstr')) )
                    )

        plotframe=masslB.frame(RooFit.Title(label),RooFit.Range('sigShortRange'))
        binData.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Name('combBkg_{0}'.format(label)),RooFit.Components('pPDF_{0}'                     .format(label)),RooFit.LineStyle(1) ,RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Name('BdBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkbarDist_BdK892MC'                  ),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Name('bDBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkbarDist_antiBdK892MC'              ),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Name('LbSig_{0}'.format(label))  ,RooFit.Components('gPDF_lbtkbarDist_antilbtkMC'                ),RooFit.LineStyle(5 ),RooFit.LineColor(2) )

        plotframe.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
        plotframe.SetMaximum( 1.2*plotframe.GetMaximum() )
        plotframe.Draw()
        plotContent=[
            ['combBkg_{0}'.format(label) ,'combinatorial background',],
            ['BdBkg_{0}'.format(label)   ,'B^{0}_{d} candidate',],
            ['bDBkg_{0}'.format(label)   ,'#bar{B^{0}_{d}} candidate',],
            ['LbSig_{0}'.format(label)   ,'#bar{#Lambda^{0}_{b}} candidate',],
            ]
        leg=createLegend(plotframe,plotContent)
        leg.Draw('same')


        canv.SaveAs('store_fig/hout_shortRangeDataFit_lBDist.eps')
        canv.SaveAs('store_fig/C_hout_shortRangeDataFit_lBDist.C')
        canv.SaveAs('store_fig/fitResult.pdf')

        if not testMode:
            fitres.Write(label)
    # fit 2016 data in Lb mass window end }}}

    if not testMode:
        outfile.Close()
canv.SaveAs('store_fig/fitResult.pdf]')
    # RooKeysPdf parameter testing example {{{
    # bkg : keyspdf
if False:
    fitLabel='lbtkbarDist_BdK892MC_TESTMode'
    mass=space.var('lbtkbarMass')
    #mass.setRange(fitLabel,5.5,7.)

    inN=inF.Get('BdToJpsiKstar892')
    #inN=inF.Get('BdToJpsiKstar1432')
    if testMode:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(4000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(4000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    else:
        dataset=RooDataSet('dataset','dataset',inN.CloneTree(40000),RooArgSet(mass))
        #dataset=RooDataSet('dataset','dataset',inN.CloneTree(40000),RooArgSet(mass,tk1Pt,tk2Pt)).reduce('tk1Pt>2.&&tk2Pt<3.')
    fitBkg=dataset.reduce(RooFit.Name('fitData_{0}'.format(fitLabel)))
    getattr(space,'import')(fitBkg)

    myFrame=mass.frame(RooFit.Title(fitLabel),RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
    dataset.plotOn(myFrame)

    ############ testing block 1 #####################
    # create target PDF.
    space.factory('KeysPdf::kPDF1_{0}(lbtkbarMass,fitData_{0},MirrorRight,1.9)'.format(fitLabel))
    space.factory('KeysPdf::kPDF2_{0}(lbtkbarMass,fitData_{0},MirrorRight,2.0)'.format(fitLabel))
    space.factory('KeysPdf::kPDF3_{0}(lbtkbarMass,fitData_{0},MirrorRight,2.2)'.format(fitLabel))
    space.pdf('kPDF1_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(40),RooFit.LineWidth(1),RooFit.Name('pdf1'))
    space.pdf('kPDF2_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(41),RooFit.LineWidth(1),RooFit.Name('pdf2'))
    space.pdf('kPDF3_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineColor(42),RooFit.LineWidth(1),RooFit.Name('pdf3'))
    plotContent=[
            ['pdf' ,'val1' ],
            ['pdf1','val2' ],
            ['pdf2','val3' ],
            ['pdf3','val4' ],
        ]
    leg=createLegend(myFrame,plotContent)
    leg.Draw('same')
    ############ testing block 1 end #################



    ############ testing block 2 #####################
    #space.factory('KeysPdf::kPDF_{0} (lbtkbarMass,fitData_{0},NoMirror           ,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF1_{0}(lbtkbarMass,fitData_{0},MirrorLeft         ,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF2_{0}(lbtkbarMass,fitData_{0},MirrorRight        ,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF3_{0}(lbtkbarMass,fitData_{0},MirrorBoth         ,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF4_{0}(lbtkbarMass,fitData_{0},MirrorAsymLeft     ,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF5_{0}(lbtkbarMass,fitData_{0},MirrorAsymRight    ,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF6_{0}(lbtkbarMass,fitData_{0},MirrorAsymLeftRight,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF7_{0}(lbtkbarMass,fitData_{0},MirrorLeftAsymRight,2.0)'.format(fitLabel))
    #space.factory('KeysPdf::kPDF8_{0}(lbtkbarMass,fitData_{0},MirrorAsymBoth     ,2.0)'.format(fitLabel))
    #space.pdf('kPDF_{0}' .format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(2 ),RooFit.Name('pdf' ))
    #space.pdf('kPDF1_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(40),RooFit.Name('pdf1'))
    #space.pdf('kPDF2_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(41),RooFit.Name('pdf2'))
    #space.pdf('kPDF3_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(42),RooFit.Name('pdf3'))
    #space.pdf('kPDF4_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(43),RooFit.Name('pdf4'))
    #space.pdf('kPDF5_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(44),RooFit.Name('pdf5'))
    #space.pdf('kPDF6_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(45),RooFit.Name('pdf6'))
    #space.pdf('kPDF7_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(46),RooFit.Name('pdf7'))
    #space.pdf('kPDF8_{0}'.format(fitLabel)).plotOn(myFrame,RooFit.LineWidth(1),RooFit.LineColor(47),RooFit.Name('pdf8'))
    #plotContent=[
    #        ['pdf' ,'NoMirror'           ],
    #        ['pdf1','MirrorLeft'         ],
    #        ['pdf2','MirrorRight'        ],
    #        ['pdf3','MirrorBoth'         ],
    #        ['pdf4','MirrorAsymLeft'     ],
    #        ['pdf5','MirrorAsymRight'    ],
    #        ['pdf6','MirrorAsymLeftRight'],
    #        ['pdf7','MirrorLeftAsymRight'],
    #        ['pdf8','MirrorAsymBoth'     ],
    #    ]
    #leg=createLegend(myFrame,plotContent)
    #leg.Draw('same')
    ############ testing block 2 end #################

    canv.cd(1)
    myFrame.Draw()
    canv.cd(2)
    myFrame.Draw()
    canv.SaveAs('store_fig/hout_mytest.eps')
    canv.SaveAs('store_fig/C_hout_mytest.C')
    canv.SaveAs('store_fig/fitResult.pdf')
    # fit bdMass in BdToJpsiKstar892 MC end }}}
