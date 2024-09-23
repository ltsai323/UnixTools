#!/usr/bin/env python
# apply cut and fit sideband only
# use dataDriven to check background

from ROOT import TLegend
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooKeysPdf


outFileName='store_root/workspace_dataBrowse_dataAndComponentsStack.root'
outFig='store_fig/pdf_workspace_dataBrowse_dataAndComponentsStack.pdf'


space=RooWorkspace('space',False)
space.factory('lbtkMass[5.3,6.0]')
space.factory('bdbarMass[2.5,8.]')
space.factory('bdMass[3.5,7.5]')
space.factory('bsMass[4.,8.]')
space.factory('kkMass[0.2,2.4]')
space.factory('kpiMass[0.5,2.2]')
space.factory('kpibarMass[0.5,2.2]')

space.factory('tk1Pt[0.,100.]')
space.factory('tk2Pt[0., 70.]')


# output workspace
outFile=TFile(outFileName,'recreate')
figDir=outFile.mkdir('figs')
fitDir=outFile.mkdir('fitRes')

# output canvas
canv=TCanvas('c1','',1000,1000)
canv.SetFillColor(4000)
canv.SetFillStyle(4000)
canv.SetFrameFillColor(4000)
canv.SetFrameFillStyle(4000)
canv.Draw(outFig+'[')

load2016Data=True
if load2016Data:
    fitLabel='dataDrivenFit'
    inFile16=TFile.Open('result_flatNtuple.root')
    inN16=inFile16.Get('2016Data')
    massLb=space.var('lbtkMass')
    massBd=space.var('bdMass')
    massbD=space.var('bdbarMass')
    massBs=space.var('bsMass')

    massKK=space.var('kkMass')
    massKp=space.var('kpiMass')
    masskP=space.var('kpibarMass')

    tk1Pt=space.var('tk1Pt')
    tk2Pt=space.var('tk2Pt')

    loadDatasetLb=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massLb,massBd,massbD,massBs,massKK,massKp,masskP,tk1Pt,tk2Pt))
    frame="lbtkMass>5.3&&lbtkMass<6."
    ptsel="tk1Pt>2. && tk2Pt>2."
    Bdbkg="((bdMass>5.25&&bdMass<5.31)&&(kpiMass>0.86&&kpiMass<0.93))"
    bDbkg="(bdbarMass>5.25&&bdbarMass<5.31&&kpibarMass<0.93)"
    bsbkg="(bsMass>5.25&&bsMass<5.4&&kkMass>1.01&&kkMass<1.03)"

    cutData=loadDatasetLb.reduce('&&'.join([frame,ptsel]))
    bkgComb=loadDatasetLb.reduce('&&'.join([frame,ptsel])+'&&'+'||'.join([Bdbkg,bDbkg,bsbkg]))

    space.factory('Polynomial::pPDF(lbtkMass,{c1[0.01,-5.,5.]})')
    keyPDF=RooKeysPdf('kPDF','kPDF',massLb,bkgComb,RooKeysPdf.NoMirror,0.1)
    getattr(space,'import')(keyPDF)
    space.factory( 'SUM::totPDF(numBKG[{initNum},0.,{maxNum}]*pPDF,{bkgNum}*kPDF)'.format(initNum=cutData.sumEntries()-bkgComb.sumEntries(),maxNum=cutData.sumEntries()*1.05,bkgNum=bkgComb.sumEntries()) )
    fitModel=space.factory('totPDF')

    massLb.setRange('leftSideband',5.3,5.619-0.03)
    massLb.setRange('rightSideband',5.619+0.03,6.)

    fitRes=fitModel.fitTo(cutData,RooFit.Minos(True),RooFit.Range('leftSideband,rightSideband'),RooFit.Save())



    plotframe=massLb.frame()
    cutData.plotOn(plotframe,RooFit.Range('leftSideband,rightSideband'),RooFit.Name('data'))
    #bkgComb.plotOn(plotframe,RooFit.MarkerColor(43))
    fitModel.plotOn(plotframe,RooFit.Name('totModel'),RooFit.LineColor( 2),RooFit.LineWidth(1), RooFit.Range('leftSideband,rightSideband'))
    fitModel.plotOn(plotframe,RooFit.Name('polyFits'),RooFit.LineColor(38),RooFit.Components('pPDF'))
    fitModel.plotOn(plotframe,RooFit.Name('particle'),RooFit.LineColor(43),RooFit.Components('kPDF'))
    #fitModel.plotOn(plotframe,RooFit.Name('bkgParticle'),RooFit.LineColor(43),RooFit.FillStyle(1),RooFit.Components('kPDF'),RooFit.DrawOption('F'),RooFit.FillStyle(3013),RooFit.Range('rightSideband'))
    #keyPDF.plotOn(plotframe,RooFit.LineColor(48))
    plotframe.Draw()
    canv.SaveAs(outFig)

    fitDir.cd()
    fitRes.Write(fitLabel)

    figDir.cd()
    plotframe.Write(fitLabel)

    plotframeForPull=massLb.frame()
    cutData.plotOn(plotframeForPull,RooFit.Range('leftSideband,rightSideband'),RooFit.Name('data'))
    fitModel.plotOn(plotframeForPull,RooFit.Name('totModel'), RooFit.Range('leftSideband,rightSideband'))
    plotframeForPull.Write(fitLabel+'ForPull')

canv.Draw(outFig+']')
outFile.cd()
space.Write()
outFile.Close()
