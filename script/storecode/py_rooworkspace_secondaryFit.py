#!/usr/bin/env python

from array import array
from ROOT import TLegend
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis, TPad, TLine, TGraphErrors, TRatioPlot, TGraph
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsData, RooPlot, RooAbsReal


outFileName='store_root/workspace_2ndStep_dataFit.root'
outFig='store_fig/pdf_workspace_2ndStep_dataFit.pdf'

outFile=TFile(outFileName,'recreate')
figDir=outFile.mkdir('figs')
fitDir=outFile.mkdir('fitRes')

# set output message level
RooMsgService.instance().setGlobalKillBelow(4)

useMinos=False
allowedNum=5.
inF=TFile.Open('result_flatNtuple.root')

def NewCanvas(name='c1'):
    canv=TCanvas(name,'',1600,1000)
    canv.SetFillColor(4000)
    canv.SetFillStyle(4000)
    return canv
canv=NewCanvas()
canv.SaveAs(outFig+'[')
TGaxis.SetMaxDigits(3)

#def SaveResult(plotframe,var,cutData,fitModel,label,fitDir,figDir):
#    print label
#    fitDir.cd()
#    fitres.Write(label)
#
#    canv.SaveAs(outFig)
#    figDir.cd()
#    plotframe.Draw()
#    plotframe.Write(label)
#
#    #plotframeForPull=RooPlot(plotframe.GetXaxis().GetXmin(),plotframe.GetXaxis().GetXmax())
#    plotframeForPull=var.frame(RooFit.Title(label+' creates for pull distribution'),RooFit.Range(plotframe.GetXaxis().GetXmin(),plotframe.GetXaxis().GetXmax()))
#    #plotframeForPull.addPlotable(cutData,'p')
#    cutData.plotOn(plotframeForPull)
#    fitModel.plotOn(plotframeForPull,RooFit.Name('totModel'))
#    plotframeForPull.Draw()
#    plotframeForPull.Write(label+'ForPull')
#    return None

def SaveResult(**kwargs):
    print '------SaveResult start {0}'.format(label)
    plotframe=kwargs['origPlot']
    var=kwargs['origVar']
    data=kwargs['data']
    tPDF=kwargs['totPDF']
    kwargs['fitDir'].cd()
    fitres.Write(kwargs['label'])

    canv.SaveAs(outFig)
    kwargs['figDir'].cd()
    plotframe.Draw()
    plotframe.Write(kwargs['label'])

    #plotframeForPull=RooPlot(plotframe.GetXaxis().GetXmin(),plotframe.GetXaxis().GetXmax())
    plotframeForPull=var.frame(RooFit.Title(kwargs['label']+' creates for pull distribution'),RooFit.Range(plotframe.GetXaxis().GetXmin(),plotframe.GetXaxis().GetXmax()))
    #plotframeForPull.addPlotable(cutData,'p')
    data['content'].plotOn(plotframeForPull,RooFit.Name('data'))
    tPDF['content'].plotOn(plotframeForPull,RooFit.Name('totModel'))
    plotframeForPull.Draw()
    plotframeForPull.Write(label+'ForPull')
    print '------SaveResult End {0}'.format(label)
    return None

space=RooWorkspace('space',False)

# new parameters
space.factory('kkMass[1.00,1.50]')
space.factory('tk1Pt[0.,100.]')
space.factory('tk2Pt[0.,100.]')
tk1Pt=space.var('tk1Pt')
tk2Pt=space.var('tk2Pt')


########## load workspace ####################
workspaceFile1=TFile.Open('store_root/workspace_0thStep_LbL0Shape.root')
lbl0LoadSpace=workspaceFile1.Get('space')
lbl0LoadSpace.SetName('lbl0LoadSpace')
widthMultiPlier=lbl0LoadSpace.var('data_MC_factor_lbl0Dist_lbl0MC')
widthMultiPlier.setConstant()
getattr(space,'import')(widthMultiPlier)

workspaceFile2=TFile.Open('store_root/workspace_1stStep_MCShape.root')
MCsLoadSpace=workspaceFile2.Get('space')
MCsLoadSpace.SetName('MCsLoadSpace')


load2016Data=True
if load2016Data:
    fitToBdfrom2016LoadData=True
    fitTobDfrom2016LoadData=True
    fitToBsfrom2016LoadData=False

    veryShortRangeFitLb=True
    veryShortRangeFitlB=False

    cleanBsfrom2016LoadData=True
    inFile16=TFile.Open('result_flatNtuple.root')
    inN16=inFile16.Get('2016Data')

    # load parameters from other workspace and import them in current workspace
    space.factory('lbtkMass[5.1,8.]')
    space.factory('lbtkbarMass[5.1,8.]')
    massLb=space.var('lbtkMass')
    masslB=space.var('lbtkbarMass')
    massBs=MCsLoadSpace.var('bsMass')
    massBd=MCsLoadSpace.var('bdMass')
    massbD=MCsLoadSpace.var('bdbarMass')
    massKK=space.var('kkMass')
    getattr(space,'import')(massBs)
    getattr(space,'import')(massBd)
    getattr(space,'import')(massbD)


    massLb.setBins(290)
    masslB.setBins(290)
    massBd.setBins(500)
    massbD.setBins(500)
    massBs.setBins(100)

    massLb.setRange('sigRangeLb',5.3,6.0)
    masslB.setRange('sigRangelB',5.3,6.0)
    massBd.setRange('sigRangeBd',5.1,5.5)
    massbD.setRange('sigRangebD',5.1,5.5)
    massBs.setRange('sigRangeBs',5.25,5.5)
    massLb.setRange('totRangeLb',massLb.getMin(),massLb.getMax())
    masslB.setRange('totRangelB',masslB.getMin(),masslB.getMax())
    massBd.setRange('totRangeBd',massBd.getMin(),massBd.getMax())
    massbD.setRange('totRangebD',massbD.getMin(),massbD.getMax())
    massBs.setRange('totRangeBs',massBs.getMin(),massBs.getMax())

    loadDatasetLb=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massLb,tk1Pt,tk2Pt))
    loadDatasetlB=RooDataSet('loadData16','loadData16',inN16,RooArgSet(masslB,tk1Pt,tk2Pt))
    loadDatasetBs=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massBs,tk1Pt,tk2Pt,massKK))
    loadDatasetBd=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massBd,tk1Pt,tk2Pt))
    loadDatasetbD=RooDataSet('loadData16','loadData16',inN16,RooArgSet(massbD,tk1Pt,tk2Pt))
    totNum=inN16.GetEntries()
    space.factory('numLb[{0},0.,{1}]'.format(2000,totNum))
    space.factory('numlB[{0},0.,{1}]'.format(2000,totNum))
    space.factory('numBs[{0},0.,{1}]'.format(totNum/4,totNum))
    space.factory('numBd[{0},0.,{1}]'.format(5000,totNum))
    space.factory('numbD[{0},0.,{1}]'.format(5000,totNum))


    # fit 2016 data in Bs mass window {{{
    if cleanBsfrom2016LoadData:
        massBs.setRange('sigRange',5.25,5.5)

        label='cleanBsFit'
        fitLabel='bsDist_BsFMC'
        #space.factory('Polynomial::pBKGs_{0}(bsMass,{{c1_{0}[0.01,-5.,5.],c2_{0}[0.01,-5.,5.]}})'.format(label))
        space.factory('Polynomial::pBKGs_{0}(bsMass,{{c1_{0}[0.01,-5.,5.]}})'.format(label))
        space.factory('bsMultiplier[1.0,0.001,5.00]')
        print 'mu_{MClabel}1'.format(MClabel=fitLabel)
        mcMean=MCsLoadSpace.var('mu_{MClabel}'.format(MClabel=fitLabel))
        mcSigma1=MCsLoadSpace.var('sigma_MC_{MClabel}1'.format(MClabel=fitLabel))
        mcSigma2=MCsLoadSpace.var('sigma_MC_{MClabel}2'.format(MClabel=fitLabel))
        mcSigma3=MCsLoadSpace.var('sigma_MC_{MClabel}3'.format(MClabel=fitLabel))
        mcFrac1=MCsLoadSpace.var('frac_{MClabel}1'.format(MClabel=fitLabel))
        mcFrac2=MCsLoadSpace.var('frac_{MClabel}2'.format(MClabel=fitLabel))

        space.factory('Product::sigma_{label}1({{bsMultiplier,{sigma} }})'.format(label=label,MClabel=fitLabel,sigma=mcSigma1.getVal()))
        space.factory('Product::sigma_{label}2({{bsMultiplier,{sigma} }})'.format(label=label,MClabel=fitLabel,sigma=mcSigma2.getVal()))
        space.factory('Product::sigma_{label}3({{bsMultiplier,{sigma} }})'.format(label=label,MClabel=fitLabel,sigma=mcSigma3.getVal()))
        space.factory('Gaussian::gPDF_{label}1(bsMass,{mean},sigma_{label}1)'.format(label=label,MClabel=fitLabel,mean=mcMean.getVal()))
        space.factory('Gaussian::gPDF_{label}2(bsMass,{mean},sigma_{label}2)'.format(label=label,MClabel=fitLabel,mean=mcMean.getVal()))
        space.factory('Gaussian::gPDF_{label}3(bsMass,{mean},sigma_{label}3)'.format(label=label,MClabel=fitLabel,mean=mcMean.getVal()))

        space.factory('SUM::gPDF_{label}({frac1}*gPDF_{label}1,{frac2}*gPDF_{label}2,gPDF_{label}3)'.format(label=label,frac1=mcFrac1.getVal(),frac2=mcFrac2.getVal()))

        totNum=loadDatasetBs.sumEntries()
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/10,totNum))
        myPDF=RooAddPdf('totBsDist','totBsDist',
                RooArgList( space.pdf('pBKGs_{0}'.format(label)),
                           #MCsLoadSpace.pdf('gPDF_MC_bsDist_BsFMC') ),
                            space.pdf('gPDF_{0}'.format(label)) ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBs') ),
                False)
        getattr(space,'import')(myPDF)



        dataset=loadDatasetBs.reduce('kkMass>1.01&&kkMass<1.03')
        #fitres=myPDF.fitTo(loadDatasetBs.binnedClone('binBs'),RooFit.Save(),RooFit.Range('sigRange'))
        fitres=myPDF.fitTo(dataset,RooFit.Save(),RooFit.Range('sigRange'),RooFit.Minos(True))

        space.var('bsMultiplier').setConstant(True)


        plotframe=massBs.frame(RooFit.Title(label),RooFit.Range('sigRange'))
        dataset.plotOn(plotframe,RooFit.Name('data'))
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2),RooFit.Name('totFit'))

        myPDF.plotOn(plotframe,RooFit.Components('gPDF_{0}'.format(label)),RooFit.LineStyle( 3),RooFit.LineColor(30),RooFit.Name('sigComp'))
        #MCsLoadSpace.pdf('gPDF_MC_{0}'.format(fitLabel)).plotOn(plotframe, RooFit.LineStyle( 3),RooFit.LineColor(43),RooFit.Name('MCShape'))

        plotframe.GetXaxis().SetTitle('J/#psi K^{+} K^{-} Mass(GeV)')
        figDir.cd()
        plotframe.Draw()
        plotframe.Write(label)
        canv.SaveAs(outFig)

        fitDir.cd()
        fitres.Write(label)
        # plot orig for check
        plotframe2=massBs.frame(RooFit.Title(label),RooFit.Range('sigRange'))
        MCsLoadSpace.pdf('gPDF_MC_{0}'.format(fitLabel)).plotOn(plotframe2)
        plotframe2.Draw()
        canv.SaveAs(outFig)
    # fit 2016 data in Bs mass window end }}}}

    # fit 2016 data in Bd mass window {{{
    if fitToBdfrom2016LoadData:
        print 'start fitToBdfrom2016LoadData'
        #massBd.setRange('sigRangeBd',5.1,5.5)

        label='BdBKG'
        space.factory('EXPR::cPDF_{0}( "bdMass>mShift_{0}?( exp(-1.*(bdMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(bdMass-mShift_{0})/cPar_{0}1) ):0.", bdMass, mShift_{0}[4.8,0.5,4.99], cPar_{0}1[1.04,0.001,100.],cPar_{0}2[0.25,0.001,10.] )'.format(label))
        space.factory('Polynomial::pPDF_{0}(bdMass,{{c1_{0}[0.01,-5.,5.]}})'.format(label))

        # load pdf from 1stStep
        mcLabel='bdDist_BdK892MC'
        mcMean  =MCsLoadSpace.var('mu_{0}'.format(mcLabel))
        mcSigma1=MCsLoadSpace.var('sigma_MC_{0}1'.format(mcLabel))
        mcSigma2=MCsLoadSpace.var('sigma_MC_{0}2'.format(mcLabel))
        mcFrac1 =MCsLoadSpace.var('frac_{0}1'.format(mcLabel))
        space.factory('Gaussian::gPartPDF_{label}1(bdMass,{muVal},sig_{label}1[{sigVal},0.0001,2.])'.format(label=mcLabel,muVal=mcMean.getVal(),sigVal=mcSigma1.getVal()))
        space.factory('Gaussian::gPartPDF_{label}2(bdMass,{muVal},sig_{label}2[{sigVal},0.0001,2.])'.format(label=mcLabel,muVal=mcMean.getVal(),sigVal=mcSigma2.getVal()))
        space.factory('SUM::gPDF_{label}(gPDF_frac1_{label}[{frac1},0.,1.]*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,frac1=mcFrac1.getVal()))

        #space.factory('gPDF_frac1_{label}[{frac1},0.,1.]'.format(label=mcLabel,frac1=mcFrac1.getVal()))
        #space.factory('gPDF_frac2_{label}[{frac2},0.,1.]'.format(label=mcLabel,frac2=mcFrac2.getVal()))
        #gauses=RooAddPdf('gPDF_{label}'.format(label=mcLabel),'gPDF_{label}'.format(label=mcLabel),
        #        RooArgList(
        #            space.pdf('gPartPDF_{label}1'.format(label=mcLabel)),
        #            space.pdf('gPartPDF_{label}2'.format(label=mcLabel)),
        #            space.pdf('gPartPDF_{label}3'.format(label=mcLabel)),
        #            ),
        #        RooArgList(
        #            space.var('gPDF_frac1_{label}'.format(label=mcLabel)),
        #            space.var('gPDF_frac2_{label}'.format(label=mcLabel)),
        #            ),
        #        True)
        #getattr(space,'import')(gauses)
        #space.factory('SUM::gPDF_{label}(gPDF_frac1_{label}[{frac1},0.,1.]*gPartPDF_{label}1,gPDF_frac2_{label}[{frac2},0.,1.]*gPartPDF_{label}2,gPartPDF_{label}3)'.format(label=mcLabel,frac1=mcFrac1.getVal(),frac2=mcFrac2.getVal()))
        #space.factory('SUM::gPDF_{label}({frac1}*gPartPDF_{label}1,{frac2}*gPartPDF_{label}2,gPartPDF_{label}3)'.format(label=mcLabel,frac1=mcFrac1.getVal(),frac2=mcFrac2.getVal()))

        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_bdDist_antiBdK892MC'))
        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_bdDist_BsFMC'))

        # add shape fraction to shape. If PDF in full mass range is 1. this shows the fraction in signal range.
        integralsig=MCsLoadSpace.pdf('kPDF_bdDist_antiBdK892MC').createIntegral(RooArgSet(massBd),RooFit.NormSet(RooArgSet(massBd)),RooFit.Range('sigRangeBd'))
        integraltot=MCsLoadSpace.pdf('kPDF_bdDist_antiBdK892MC').createIntegral(RooArgSet(massBd),RooFit.NormSet(RooArgSet(massBd)),RooFit.Range('totRangeBd'))
        integralsigBs=MCsLoadSpace.pdf('kPDF_bdDist_BsFMC').createIntegral(RooArgSet(massBd),RooFit.NormSet(RooArgSet(massBd)),RooFit.Range('sigRangeBd'))
        integraltotBs=MCsLoadSpace.pdf('kPDF_bdDist_BsFMC').createIntegral(RooArgSet(massBd),RooFit.NormSet(RooArgSet(massBd)),RooFit.Range('totRangeBd'))
        space.factory('kPDF_factor_bD[{fracVal}]'.format(fracVal=(integralsig.getVal()/integraltot.getVal())))
        space.factory('kPDF_Bdfactor_bDNum[{fracVal}]'.format(fracVal=(integralsig.getVal()/integraltot.getVal())))
        space.factory('kPDF_Bdfactor_BsNum[{fracVal}]'.format(fracVal=(integralsigBs.getVal()/integraltotBs.getVal())))
        space.factory('Product::fracbDNum_inBd({{kPDF_Bdfactor_bDNum,numbD}})')
        space.factory('Product::fracBsNum_inBd({{kPDF_Bdfactor_BsNum,numBs}})')

        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/2,totNum))
        space.factory(
                'SUM::totFit_{label}({num1}*{pdf1},{num2}*{pdf2},{num3}*{pdf3},{num4}*{pdf4})'.format(
                    label=label,
                    num1='numCombBkg_{0}'.format(label),
                    pdf1='cPDF_{0}'.format(label),
                    #pdf1='pPDF_{0}'.format(label),
                    num2='numBd',
                    pdf2='gPDF_{0}'.format(mcLabel),
                    num3='fracbDNum_inBd',
                    pdf3='kPDF_bdDist_antiBdK892MC',
                    num4='fracBsNum_inBd',
                    pdf4='kPDF_bdDist_BsFMC',
                    )
                )
        myPDF=space.pdf('totFit_{label}'.format(label=label))
        #myPDF=RooAddPdf('totFit_{0}'.format(label), 'totFit_{0}'.format(label),
        #        RooArgList( space.pdf('cPDF_{0}'.format(label)),
        #                    space.pdf('gPDF_{label}'.format(label=mcLabel)),
        #                    #MCsLoadSpace.pdf('gPDF_MC_{label}'.format(label=mcLabel)),
        #                    MCsLoadSpace.pdf('kPDF_bdDist_antiBdK892MC'),
        #                    MCsLoadSpace.pdf('kPDF_bdDist_BsFMC') ),
        #        RooArgList( space.var('numCombBkg_{0}'.format(label)),
        #                    space.var('numBd'),
        #                    space.var('fracNumbD'),
        #                    space.var('numBs') ),
        #        False)
        #getattr(space,'import')(myPDF)




        #binData=loadDatasetBd.reduce('tk1Pt>3.&&tk2Pt>2.').binnedClone('binBd')
        binData=loadDatasetBd.binnedClone('binBd')
        fitres=myPDF.fitTo(binData,RooFit.Range('sigRangeBd'),RooFit.Save(),RooFit.Minos(useMinos))
        var=space.var('numBd')
        space.factory('Gaussian::numBdConstr(numBd,{0},{1})'.format(var.getVal(),var.getError()))


        plotframe=massBd.frame(RooFit.Title(label),RooFit.Range('sigRangeBd'))
        binData.plotOn(plotframe, RooFit.Name('data'))
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2), RooFit.Name('totFit'),RooFit.Range('sigRangeBd'))
        myPDF.plotOn(plotframe,RooFit.Components('cPDF_{label}'       .format(label=label)),RooFit.LineStyle(2),RooFit.LineColor(13), RooFit.Name('combBKG'))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_{mcLabel}'       .format(mcLabel=mcLabel)),RooFit.LineStyle(10),RooFit.LineColor(30), RooFit.Name('sigComp'))
        #myPDF.plotOn(plotframe,RooFit.Components('gPDF_MC_{mcLabel}'       .format(mcLabel=mcLabel)),RooFit.LineStyle(10),RooFit.LineColor(30), RooFit.Name('sigComp'))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bdDist_antiBdK892MC'                 ),RooFit.LineStyle(10),RooFit.LineColor(38),RooFit.Name('bDBKG'))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bdDist_BsFMC'                        ),RooFit.LineStyle( 8),RooFit.LineColor(40),RooFit.Name('BsBKG'))

        plotframe.GetXaxis().SetTitle('J/#psi K^{+} #pi^{-} Mass(GeV)')
        plotframe.Draw()

        SaveResult(
                origPlot=plotframe,
                origVar=massBd,
                data={'content':binData,'range':'sigRangeBd'},
                totPDF={'content':myPDF,'range':'sigRangeBd'},
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )

        if True:
            fitres=myPDF.fitTo(binData,RooFit.Range('sigRangeBd'),RooFit.Save(),RooFit.Minos(useMinos), RooFit.RefreshNorm())
            evar=space.var('numBd')
            space.factory('Gaussian::numBdConstr(numBd,{0},{1})'.format(evar.getVal(),evar.getError()))


            lplotframe=massBd.frame(RooFit.Title(label),RooFit.Range('sigRangeBd'),RooFit.Name('hi'))
            binData.plotOn(lplotframe, RooFit.Name('data'), RooFit.RefreshNorm())
            myPDF.plotOn(lplotframe,RooFit.LineWidth(1),RooFit.LineColor(2), RooFit.Name('totFit'),RooFit.Range('sigRangeBd'),
                RooFit.Normalization( 54951.,RooAbsReal.NumEvent),
                )
            myPDF.plotOn(lplotframe,RooFit.Components('cPDF_{label}'       .format(label=label)),RooFit.LineStyle(2),RooFit.LineColor(13), RooFit.Name('combBKG'))
            myPDF.plotOn(lplotframe,RooFit.Components('gPDF_{mcLabel}'       .format(mcLabel=mcLabel)),RooFit.LineStyle(10),RooFit.LineColor(30), RooFit.Name('sigComp'))
            #myPDF.plotOn(lplotframe,RooFit.Components('gPDF_MC_{mcLabel}'       .format(mcLabel=mcLabel)),RooFit.LineStyle(10),RooFit.LineColor(30), RooFit.Name('sigComp'))
            myPDF.plotOn(lplotframe,RooFit.Components('kPDF_bdDist_antiBdK892MC'                 ),RooFit.LineStyle(10),RooFit.LineColor(38),RooFit.Name('bDBKG'))
            myPDF.plotOn(lplotframe,RooFit.Components('kPDF_bdDist_BsFMC'                        ),RooFit.LineStyle( 8),RooFit.LineColor(40),RooFit.Name('BsBKG'))

            lplotframe.GetXaxis().SetTitle('J/#psi K^{+} #pi^{-} Mass(GeV)')
            lplotframe.Draw()

            SaveResult(
                    origPlot=lplotframe,
                    origVar=massBd,
                    data={'content':binData,'range':'sigRangeBd'},
                    totPDF={'content':myPDF,'range':'sigRangeBd'},
                    label='testBdSecFit',
                    fitDir=fitDir,
                    figDir=figDir,
                    )

        space.var('sig_{label}1'.format(label=mcLabel)).setConstant(True)
        space.var('sig_{label}2'.format(label=mcLabel)).setConstant(True)
        space.var('gPDF_frac1_{label}'.format(label=mcLabel)).setConstant(True)
        space.var('cPar_{label}1' .format(label=label)).setConstant(True)
        space.var('cPar_{label}2' .format(label=label)).setConstant(True)
        space.var('mShift_{label}'.format(label=label)).setConstant(True)
        #space.var('numBd').setConstant(True)
        print 'end    fitToBdfrom2016LoadData'
    # fit 2016 data in Bd mass window end }}}
    # fit 2016 data in BdBar mass window {{{
    if fitTobDfrom2016LoadData:

        label='bDBKG'
        space.factory('EXPR::cPDF_{0}( "bdbarMass>mShift_{0}?( exp(-1.*(bdbarMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(bdbarMass-mShift_{0})/cPar_{0}1) ):0.", bdbarMass, mShift_{0}[4.8,0.5,4.99], cPar_{0}1[1.04,0.001,100.],cPar_{0}2[0.25,0.001,10.] )'.format(label))
        space.factory('Polynomial::pPDF_{0}(bdbarMass,{{c1_{0}[0.01,-5.,5.]}})'.format(label))

        # load pdf from 1stStep
        mcLabel='bdbarDist_antiBdK892MC'
        mcMean  =MCsLoadSpace.var('mu_{0}'.format(mcLabel))
        mcSigma1=MCsLoadSpace.var('sigma_MC_{0}1'.format(mcLabel))
        mcSigma2=MCsLoadSpace.var('sigma_MC_{0}2'.format(mcLabel))
        mcFrac1 =MCsLoadSpace.var('frac_{0}1'.format(mcLabel))
        #space.factory('Product::sigma_{label}1({{bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma=mcSigma1.getVal()))
        #space.factory('Product::sigma_{label}2({{bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma=mcSigma2.getVal()))
        #space.factory('Product::sigma_{label}3({{bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma=mcSigma3.getVal()))
        space.factory('Gaussian::gPartPDF_{label}1(bdbarMass,{muVal},sig_{label}1[{sigVal},0.0001,0.05])'.format(label=mcLabel,muVal=mcMean.getVal(),sigVal=mcSigma1.getVal()))
        space.factory('Gaussian::gPartPDF_{label}2(bdbarMass,{muVal},sig_{label}2[{sigVal},0.0001,0.05])'.format(label=mcLabel,muVal=mcMean.getVal(),sigVal=mcSigma2.getVal()))
        space.factory('SUM::gPDF_{label}(gPDF_frac1_{label}[{frac1},0.,1.]*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,frac1=mcFrac1.getVal()))

        # add shape fraction to shape. If PDF in full mass range is 1. this shows the fraction in signal range.
        integralsig=MCsLoadSpace.pdf('kPDF_bdbarDist_BdK892MC').createIntegral(RooArgSet(massbD),RooFit.NormSet(RooArgSet(massbD)),RooFit.Range('sigRangebD'))
        integraltot=MCsLoadSpace.pdf('kPDF_bdbarDist_BdK892MC').createIntegral(RooArgSet(massbD),RooFit.NormSet(RooArgSet(massbD)),RooFit.Range('totRangebD'))
        integralsigBs=MCsLoadSpace.pdf('kPDF_bdbarDist_BsFMC').createIntegral(RooArgSet(massbD),RooFit.NormSet(RooArgSet(massbD)),RooFit.Range('sigRangebD'))
        integraltotBs=MCsLoadSpace.pdf('kPDF_bdbarDist_BsFMC').createIntegral(RooArgSet(massbD),RooFit.NormSet(RooArgSet(massbD)),RooFit.Range('totRangebD'))
        space.factory('kPDF_bDfactor_BdNum[{fracVal}]'.format(fracVal=(integralsig.getVal()/integraltot.getVal())))
        space.factory('kPDF_bDfactor_BsNum[{fracVal}]'.format(fracVal=(integralsigBs.getVal()/integraltotBs.getVal())))
        space.factory('Product::fracBdNum_inbD({{kPDF_bDfactor_BdNum,numBd}})')
        space.factory('Product::fracBsNum_inbD({{kPDF_bDfactor_BsNum,numBs}})')

        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_bdbarDist_BdK892MC'))
        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_bdbarDist_BsFMC'))
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label,totNum/2,totNum))
        space.factory(
                'SUM::totFit_{label}({num1}*{pdf1},{num2}*{pdf2},{num3}*{pdf3},{num4}*{pdf4})'.format(
                    label=label,
                    num1='numCombBkg_{0}'.format(label),
                    pdf1='cPDF_{0}'.format(label),
                    #pdf1='pPDF_{0}'.format(label),
                    num2='fracBdNum_inbD',
                    pdf2='kPDF_bdbarDist_BdK892MC',
                    num3='numbD',
                    pdf3='gPDF_{label}'.format(label=mcLabel),
                    num4='fracBsNum_inbD',
                    pdf4='kPDF_bdbarDist_BsFMC',
                    )
                )
        myPDF=space.pdf('totFit_{label}'.format(label=label))


        #binData=loadDatasetBd.reduce('tk1Pt>3.&&tk2Pt>2.').binnedClone('binBd')
        binData=loadDatasetbD.binnedClone('binbD')
        fitres=myPDF.fitTo(binData,RooFit.Range('sigRangebD'),RooFit.Save(),RooFit.Minos(useMinos))
        var=space.var('numbD')
        space.factory('Gaussian::numbDConstr(numbD,{0},{1})'.format(var.getVal(),var.getError()))


        plotframe=massbD.frame(RooFit.Title(label),RooFit.Range('sigRangebD'))
        binData.plotOn(plotframe, RooFit.Name('data'))
        myPDF.plotOn(plotframe,
                RooFit.LineWidth( 1),RooFit.LineColor( 2),RooFit.Name('totFit'))
        myPDF.plotOn(plotframe,RooFit.Components('cPDF_{label}'.format(label=label)),
                RooFit.LineStyle( 2),RooFit.LineColor(13),RooFit.Name('combBKG'))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_{mcLabel}'.format(mcLabel=mcLabel)),
                RooFit.LineStyle(10),RooFit.LineColor(38),RooFit.Name('sigComp'))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bdbarDist_BdK892MC'),
                RooFit.LineStyle(10),RooFit.LineColor(30),RooFit.Name('bDBKG'))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bdbarDist_BsFMC'),
                RooFit.LineStyle( 8),RooFit.LineColor(40),RooFit.Name('BsBKG'))

        plotframe.GetXaxis().SetTitle('J/#psi K^{-} #pi^{+} Mass(GeV)')
        plotframe.Draw()
        SaveResult(
                origPlot=plotframe,
                origVar=massbD,
                data={'content':binData,'range':'sigRangebD'},
                totPDF={'content':myPDF,'range':'sigRangebD'},
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )

        space.var('sig_{label}1'.format(label=mcLabel)).setConstant(True)
        space.var('sig_{label}2'.format(label=mcLabel)).setConstant(True)
        space.var('gPDF_frac1_{label}'.format(label=mcLabel)).setConstant(True)

        space.var('cPar_{label}1' .format(label=label)).setConstant(True)
        space.var('cPar_{label}2' .format(label=label)).setConstant(True)
        space.var('mShift_{label}'.format(label=label)).setConstant(True)
    # fit 2016 data in BdBar mass window end }}}

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
                            MCsLoadSpace.pdf('kPDF_bsDist_BdK892MC'),
                            MCsLoadSpace.pdf('kPDF_bsDist_antiBdK892MC'),
                            MCsLoadSpace.pdf('gPDF_MC_bsDist_BsFMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD'),
                            space.var('numBs') ),
                False)
        getattr(space,'import')(myPDF)



        fitres=myPDF.fitTo(loadDatasetBs.binnedClone('binBs'),RooFit.Save(),RooFit.Range('sigRange'))


        plotframe=massBs.frame(RooFit.Title(label),RooFit.Range('sigRange'))
        loadDatasetBs.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))

        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_BdK892MC'       .format(label)),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_antiBdK892MC'   .format(label)),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Components('gPDF_MC_bsDist_BsFMC'          .format(label)),RooFit.LineStyle(3 ),RooFit.LineColor(2 ))
        #myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_lbtkMC'         .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(41))
        #myPDF.plotOn(plotframe,RooFit.Components('kPDF_bsDist_antilbtkMC'     .format(label)),RooFit.LineStyle(5 ),RooFit.LineColor(46))

        plotframe.GetXaxis().SetTitle('J/#psi K^{+} K^{-} Mass(GeV)')
        #plotframe.Draw()
        #canv.SaveAs(outFig)
        #figDir.cd()
        #plotframe.Draw()
        #plotframe.Write(label)

        #fitDir.cd()
        #fitres.Write(label)
        SaveResult(
                origPlot=plotframe,
                origVar=massBs,
                data={'content':binData, 'range':'sigRange'},
                totPDF={'content':myPDF, 'range':'sigRange'},
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )
    # fit 2016 data in Bs mass window end }}}}

    canv.Clear()
    canv.SetFillColor(4000)
    canv.SetFillStyle(4000)
    canv.cd()


    print 'jjj ee'
    # fit 2016 data in short range Lb mass window {{{
    if veryShortRangeFitLb:

        label='ShortRangeLbFit'
        space.factory('Polynomial::pPDF_{0}'.format(label)+'(lbtkMass,{cp1[0.01,-5.,5.],cp2[0.01,-5.,5.]})')
        space.factory('Exponential::ePDF_{0}'.format(label)+'(lbtkMass,ce1[0.2,-10.,1.])')
        space.factory('EXPR::cPDF_{0}( "lbtkMass>mShift_{0}?( exp(-1.*(lbtkMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(lbtkMass-mShift_{0})/cPar_{0}1) ):0.", lbtkMass, mShift_{0}[4.8,4.0,5.2], cPar_{0}1[0.44,0.001,100.],cPar_{0}2[0.0025,0.0000001,10.] )'.format(label))
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label, totNum,totNum))

        # load pdf from 1stStep
        mcLabel='lbtkDist_lbtkMC'
        getattr(space,'import')(MCsLoadSpace.var('mu_{0}'.format(mcLabel)))
        getattr(space,'import')(MCsLoadSpace.var('sigma_MC_{0}1'.format(mcLabel)))
        getattr(space,'import')(MCsLoadSpace.var('sigma_MC_{0}2'.format(mcLabel)))
        getattr(space,'import')(MCsLoadSpace.var('frac_{0}1'.format(mcLabel)))
        mcMean  =space.var('mu_{0}'.format(mcLabel))
        mcSigma1=space.var('sigma_MC_{0}1'.format(mcLabel))
        mcSigma2=space.var('sigma_MC_{0}2'.format(mcLabel))
        mcFrac1 =space.var('frac_{0}1'.format(mcLabel))
        mcMean  .setConstant(True)
        mcSigma1.setConstant(True)
        mcSigma2.setConstant(True)
        mcFrac1 .setConstant(True)
        space.factory('Product::sigma_{label}1({{bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma=mcSigma1.GetName()))
        space.factory('Product::sigma_{label}2({{bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma=mcSigma1.GetName()))
        space.factory('Gaussian::gPartPDF_{label}1(lbtkMass,{muVal},{sigma})'.format(label=mcLabel,muVal=mcMean.GetName(),sigma=mcSigma1.GetName()))
        space.factory('Gaussian::gPartPDF_{label}2(lbtkMass,{muVal},{sigma})'.format(label=mcLabel,muVal=mcMean.GetName(),sigma=mcSigma2.GetName()))
        space.factory('SUM::gPDF_{label}({frac1}*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,frac1=mcFrac1.GetName()))

        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_lbtkDist_BdK892MC'))
        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_lbtkDist_antiBdK892MC'))
        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_lbtkDist_BsFMC'))

        # add shape fraction to shape. If PDF in full mass range is 1. this shows the fraction in signal range.
        integralsigBd=space.pdf('kPDF_lbtkDist_BdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('sigRangeLb'))
        integraltotBd=space.pdf('kPDF_lbtkDist_BdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('totRangeLb'))
        integralsigbD=space.pdf('kPDF_lbtkDist_antiBdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('sigRangeLb'))
        integraltotbD=space.pdf('kPDF_lbtkDist_antiBdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('totRangeLb'))
        integralsigBs=space.pdf('kPDF_lbtkDist_BsFMC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('sigRangeLb'))
        integraltotBs=space.pdf('kPDF_lbtkDist_BsFMC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('totRangeLb'))
        space.factory('kPDF_Lbfactor_BdNum[{fracVal}]'.format(fracVal=(integralsigBd.getVal()/integraltotBd.getVal())))
        space.factory('kPDF_Lbfactor_bDNum[{fracVal}]'.format(fracVal=(integralsigbD.getVal()/integraltotbD.getVal())))
        space.factory('kPDF_Lbfactor_BsNum[{fracVal}]'.format(fracVal=(integralsigBs.getVal()/integraltotBs.getVal())))
        space.factory('Product::fracBdNum_inLb({{kPDF_Lbfactor_BdNum,numBd}})')
        space.factory('Product::fracbDNum_inLb({{kPDF_Lbfactor_bDNum,numbD}})')
        space.factory('Product::fracBsNum_inLb({{kPDF_Lbfactor_BsNum,numBs}})')

        print 'fracBd : {0}/{1} = {2}'.format(integralsigBd.getVal(),integraltotBd.getVal(),integralsigBd.getVal()/integraltotBd.getVal())
        print 'fracbD : {0}/{1} = {2}'.format(integralsigbD.getVal(),integraltotbD.getVal(),integralsigbD.getVal()/integraltotbD.getVal())
        print 'fracBs : {0}/{1} = {2}'.format(integralsigBs.getVal(),integraltotBs.getVal(),integralsigBs.getVal()/integraltotBs.getVal())



        space.factory(
                'SUM::totFit_{label}({num1}*{pdf1},{num2}*{pdf2},{num3}*{pdf3},{num4}*{pdf4},{num5}*{pdf5})'.format(
                    label=label,
                    num1='numCombBkg_{0}'.format(label),
                    pdf1='pPDF_{0}'.format(label),
                    num2='fracBdNum_inLb',
                    pdf2='kPDF_lbtkDist_BdK892MC',
                    num3='fracbDNum_inLb',
                    pdf3='kPDF_lbtkDist_antiBdK892MC',
                    num4='fracBsNum_inLb',
                    pdf4='kPDF_lbtkDist_BsFMC',
                    num5='numLb',
                    pdf5='gPDF_{label}'.format(label=mcLabel)
                    )
                )
        myPDF=space.pdf('totFit_{label}'.format(label=label))
        #myPDF=RooAddPdf('smallLbDist','smallLbDist',
        #        RooArgList( space.pdf('pPDF_{0}'.format(label)),
        #                    MCsLoadSpace.pdf('kPDF_lbtkDist_BdK892MC'),
        #                    MCsLoadSpace.pdf('kPDF_lbtkDist_antiBdK892MC'),
        #                    MCsLoadSpace.pdf('kPDF_lbtkDist_BsFMC'),
        #                    space.pdf('gPDF_{label}'.format(label=mcLabel)) ),
        #        RooArgList( space.var('numCombBkg_{0}'.format(label)),
        #                    space.var('fracBdNum_inLb'),
        #                    space.var('fracbDNum_inLb'),
        #                    space.var('fracBsNum_inLb'),
        #                    space.var('numLb') ),
        #        False)
        #getattr(space,'import')(myPDF)

        #binData=loadDatasetLb.reduce('tk1Pt>3.&&tk2Pt>2.').binnedClone('shortBinLb')
        binData=loadDatasetLb.reduce('tk1Pt>1.&&tk2Pt>1.').binnedClone('shortBinLb')
        #binData=loadDatasetLb.binnedClone('shortBinLb')
        #binData=loadDatasetLb


        fitres=myPDF.fitTo(binData,RooFit.Range('sigRangeLb'),RooFit.Save(),RooFit.Minos(useMinos))

        plotframe=massLb.frame(RooFit.Title(label),RooFit.Range('sigRangeLb'))
        binData.plotOn(plotframe,RooFit.Name('data'))
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Name('combBkg_{0}'.format(label)),RooFit.Components('pPDF_{0}'.format(label)                     ),RooFit.LineStyle( 1),RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Name('BdBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_BdK892MC'                     ),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Name('bDBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_antiBdK892MC'                 ),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Name('BsBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_BsFMC'                        ),RooFit.LineStyle(10),RooFit.LineColor(48))
        myPDF.plotOn(plotframe,RooFit.Name('LbSig_{0}'.format(label))  ,RooFit.Components('gPDF_{label}'.format(label=mcLabel)         ),RooFit.LineStyle( 5),RooFit.LineColor( 2))

        plotframe.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
        plotframe.Draw()
        plotContent=[
            ['combBkg_{0}'.format(label) ,'combinatorial background',],
            ['BdBkg_{0}'.format(label)   ,'B^{0}_{d} candidate',],
            ['bDBkg_{0}'.format(label)   ,'#bar{B}^{0}_{d} candidate',],
            ['LbSig_{0}'.format(label)   ,'#Lambda^{0}_{b} candidate',],
            ['BsBkg_{0}'.format(label)   ,'#B^{0}_{s} candidate',],
            ]



        #fitDir.cd()
        #fitres.Write(label)

        #canv.SaveAs(outFig)
        #figDir.cd()
        #plotframe.Draw()
        #plotframe.Write(label)

        #plotframeForPull=massLb.frame()
        #cutData.plotOn(plotframeForPull,RooFit.Name('data'))
        #fitModel.plotOn(plotframeForPull,RooFit.Name('totModel'))
        #plotframeForPull.Write(fitLabel+'ForPull')
        SaveResult(
                origPlot=plotframe,
                origVar=massLb,
                data={'content':binData, 'range':'sigRangeLb'},
                totPDF={'content':myPDF, 'range':'sigRangeLb'},
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )
    # fit 2016 data in Lb mass window end }}}
    # fit 2016 data in short range lB mass window {{{
    if False:
    #if veryShortRangeFitlB:

        label='ShortRangelBFit'
        space.factory('Polynomial::pPDF_{0}'.format(label)+'(lbtkbarMass,{cp1_[0.01,-5.,5.],cp2_[0.01,-5.,5.]})')
        space.factory('Exponential::ePDF_{0}'.format(label)+'(lbtkbarMass,ce1[0.2,-10.,1.])')
        #space.factory('EXPR::cPDF_{0}( "lbtkbarMass>mShift_{0}?( exp(-1.*(lbtkbarMass-mShift_{0})/(cPar_{0}1+cPar_{0}2)) - exp(-1.*(lbtkbarMass-mShift_{0})/cPar_{0}1) ):0.", lbtkbarMass, mShift_{0}[4.8,4.0,5.2], cPar_{0}1[0.44,0.001,100.],cPar_{0}2[0.0025,0.0000001,10.] )'.format(label))
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label, totNum,totNum))

        # load pdf from 1stStep
        mcLabel='lbtkbarDist_antilbtkMC'
        getattr(space,'import')(MCsLoadSpace.var('mu_{0}'.format(mcLabel)))
        getattr(space,'import')(MCsLoadSpace.var('sigma_MC_{0}1'.format(mcLabel)))
        getattr(space,'import')(MCsLoadSpace.var('sigma_MC_{0}2'.format(mcLabel)))
        getattr(space,'import')(MCsLoadSpace.var('frac_{0}1'.format(mcLabel)))
        mcMean  =space.var('mu_{0}'.format(mcLabel))
        mcSigma1=space.var('sigma_MC_{0}1'.format(mcLabel))
        mcSigma2=space.var('sigma_MC_{0}2'.format(mcLabel))
        mcFrac1 =space.var('frac_{0}1'.format(mcLabel))
        mcMean  .setConstant(True)
        mcSigma1.setConstant(True)
        mcSigma2.setConstant(True)
        mcFrac1 .setConstant(True)
        space.factory('Product::sigma_{label}1({{bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma=mcSigma1.GetName()))
        space.factory('Product::sigma_{label}2({{bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma=mcSigma1.GetName()))
        space.factory('Gaussian::gPartPDF_{label}1(lbtkbarMass,{muVal},{sigma})'.format(label=mcLabel,muVal=mcMean.GetName(),sigma=mcSigma1.GetName()))
        space.factory('Gaussian::gPartPDF_{label}2(lbtkbarMass,{muVal},{sigma})'.format(label=mcLabel,muVal=mcMean.GetName(),sigma=mcSigma2.GetName()))
        space.factory('SUM::gPDF_{label}({frac1}*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,frac1=mcFrac1.GetName()))

        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_lbtkDist_BdK892MC'))
        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_lbtkDist_antiBdK892MC'))
        getattr(space,'import')(MCsLoadSpace.pdf('kPDF_lbtkDist_BsFMC'))

        # add shape fraction to shape. If PDF in full mass range is 1. this shows the fraction in signal range.
        integralsigBd=space.pdf('kPDF_lbtkDist_BdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('sigRangeLb'))
        integraltotBd=space.pdf('kPDF_lbtkDist_BdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('totRangeLb'))
        integralsigbD=space.pdf('kPDF_lbtkDist_antiBdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('sigRangeLb'))
        integraltotbD=space.pdf('kPDF_lbtkDist_antiBdK892MC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('totRangeLb'))
        integralsigBs=space.pdf('kPDF_lbtkDist_BsFMC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('sigRangeLb'))
        integraltotBs=space.pdf('kPDF_lbtkDist_BsFMC').createIntegral(RooArgSet(massLb),RooFit.NormSet(RooArgSet(massLb)),RooFit.Range('totRangeLb'))
        space.factory('kPDF_Lbfactor_BdNum[{fracVal}]'.format(fracVal=(integralsigBd.getVal()/integraltotBd.getVal())))
        space.factory('kPDF_Lbfactor_bDNum[{fracVal}]'.format(fracVal=(integralsigbD.getVal()/integraltotbD.getVal())))
        space.factory('kPDF_Lbfactor_BsNum[{fracVal}]'.format(fracVal=(integralsigBs.getVal()/integraltotBs.getVal())))
        space.factory('Product::fracBdNum_inLb({{kPDF_Lbfactor_BdNum,numBd}})')
        space.factory('Product::fracbDNum_inLb({{kPDF_Lbfactor_bDNum,numbD}})')
        space.factory('Product::fracBsNum_inLb({{kPDF_Lbfactor_BsNum,numBs}})')

        print 'fracBd : {0}/{1} = {2}'.format(integralsigBd.getVal(),integraltotBd.getVal(),integralsigBd.getVal()/integraltotBd.getVal())
        print 'fracbD : {0}/{1} = {2}'.format(integralsigbD.getVal(),integraltotbD.getVal(),integralsigbD.getVal()/integraltotbD.getVal())
        print 'fracBs : {0}/{1} = {2}'.format(integralsigBs.getVal(),integraltotBs.getVal(),integralsigBs.getVal()/integraltotBs.getVal())



        space.factory(
                'SUM::totFit_{label}({num1}*{pdf1},{num2}*{pdf2},{num3}*{pdf3},{num4}*{pdf4},{num5}*{pdf5})'.format(
                    label=label,
                    num1='numCombBkg_{0}'.format(label),
                    pdf1='pPDF_{0}'.format(label),
                    num2='fracBdNum_inLb',
                    pdf2='kPDF_lbtkDist_BdK892MC',
                    num3='fracbDNum_inLb',
                    pdf3='kPDF_lbtkDist_antiBdK892MC',
                    num4='fracBsNum_inLb',
                    pdf4='kPDF_lbtkDist_BsFMC',
                    num5='numLb',
                    pdf5='gPDF_{label}'.format(label=mcLabel)
                    )
                )
        myPDF=space.pdf('totFit_{label}'.format(label=label))
        #myPDF=RooAddPdf('smallLbDist','smallLbDist',
        #        RooArgList( space.pdf('pPDF_{0}'.format(label)),
        #                    MCsLoadSpace.pdf('kPDF_lbtkDist_BdK892MC'),
        #                    MCsLoadSpace.pdf('kPDF_lbtkDist_antiBdK892MC'),
        #                    MCsLoadSpace.pdf('kPDF_lbtkDist_BsFMC'),
        #                    space.pdf('gPDF_{label}'.format(label=mcLabel)) ),
        #        RooArgList( space.var('numCombBkg_{0}'.format(label)),
        #                    space.var('fracBdNum_inLb'),
        #                    space.var('fracbDNum_inLb'),
        #                    space.var('fracBsNum_inLb'),
        #                    space.var('numLb') ),
        #        False)
        #getattr(space,'import')(myPDF)

        #binData=loadDatasetLb.reduce('tk1Pt>3.&&tk2Pt>2.').binnedClone('shortBinLb')
        binData=loadDatasetLb.reduce('tk1Pt>1.&&tk2Pt>1.').binnedClone('shortBinLb')
        #binData=loadDatasetLb.binnedClone('shortBinLb')
        #binData=loadDatasetLb


        fitres=myPDF.fitTo(binData,RooFit.Range('sigRangeLb'),RooFit.Save(),RooFit.Minos(useMinos))

        plotframe=massLb.frame(RooFit.Title(label),RooFit.Range('sigRangeLb'))
        binData.plotOn(plotframe,RooFit.Name('data'))
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Name('combBkg_{0}'.format(label)),RooFit.Components('pPDF_{0}'.format(label)                     ),RooFit.LineStyle( 1),RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Name('BdBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_BdK892MC'                     ),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Name('bDBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_antiBdK892MC'                 ),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Name('BsBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkDist_BsFMC'                        ),RooFit.LineStyle(10),RooFit.LineColor(48))
        myPDF.plotOn(plotframe,RooFit.Name('LbSig_{0}'.format(label))  ,RooFit.Components('gPDF_{label}'.format(label=mcLabel)         ),RooFit.LineStyle( 5),RooFit.LineColor( 2))

        plotframe.GetXaxis().SetTitle('J/#psi p K^{-} Mass(GeV)')
        plotframe.Draw()
        plotContent=[
            ['combBkg_{0}'.format(label) ,'combinatorial background',],
            ['BdBkg_{0}'.format(label)   ,'B^{0}_{d} candidate',],
            ['bDBkg_{0}'.format(label)   ,'#bar{B}^{0}_{d} candidate',],
            ['LbSig_{0}'.format(label)   ,'#Lambda^{0}_{b} candidate',],
            ['BsBkg_{0}'.format(label)   ,'#B^{0}_{s} candidate',],
            ]



        #fitDir.cd()
        #fitres.Write(label)

        #canv.SaveAs(outFig)
        #figDir.cd()
        #plotframe.Draw()
        #plotframe.Write(label)

        #plotframeForPull=massLb.frame()
        #cutData.plotOn(plotframeForPull,RooFit.Name('data'))
        #fitModel.plotOn(plotframeForPull,RooFit.Name('totModel'))
        #plotframeForPull.Write(fitLabel+'ForPull')
        SaveResult(
                origPlot=plotframe,
                origVar=massLb,
                data={'content':binData, 'range':'sigRangeLb'},
                totPDF={'content':myPDF, 'range':'sigRangeLb'},
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )
    # fit 2016 data in Lb mass window end }}}
    # fit 2016 data in short range lB mass window {{{
    if False:
    #if veryShortRangeFitlB:

        label='ShortRangelBFit'
        space.factory('Polynomial::pPDF_{0}'.format(label)+'(lbtkbarMass,{c1[0.01,-5.,5.],c2[0.01,-5.,5.]})')
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label, totNum,totNum))
        myPDF=RooAddPdf('smalllBDist','smalllBDist',
                RooArgList( space.pdf('pPDF_{0}'.format(label)),
                            MCsLoadSpace.pdf('kPDF_lbtkbarDist_BdK892MC'),
                            MCsLoadSpace.pdf('kPDF_lbtkbarDist_antiBdK892MC'),
                            MCsLoadSpace.pdf('gPDF_MC_lbtkbarDist_antilbtkMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numBd'),
                            space.var('numbD'),
                            space.var('numlB') ),
                False)
        getattr(space,'import')(myPDF)

        binData=loadDatasetlB.binnedClone('shortBinlB')

        #fitres=myPDF.fitTo(binData,RooFit.Range('sigRangeLb'),RooFit.Save(),RooFit.Minos(False),
        #        RooFit.ExternalConstraints( RooArgSet(space.pdf('numbDConstr'),space.pdf('numBdConstr')) )
        #            )

        plotframe=masslB.frame(RooFit.Title(label),RooFit.Range('sigRangeLb'))
        binData.plotOn(plotframe)
        myPDF.plotOn(plotframe,RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Name('combBkg_{0}'.format(label)),RooFit.Components('pPDF_{0}'                     .format(label)),RooFit.LineStyle(1) ,RooFit.LineColor(41))
        myPDF.plotOn(plotframe,RooFit.Name('BdBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkbarDist_BdK892MC'                  ),RooFit.LineStyle(10),RooFit.LineColor(30))
        myPDF.plotOn(plotframe,RooFit.Name('bDBkg_{0}'.format(label))  ,RooFit.Components('kPDF_lbtkbarDist_antiBdK892MC'              ),RooFit.LineStyle(10),RooFit.LineColor(38))
        myPDF.plotOn(plotframe,RooFit.Name('LbSig_{0}'.format(label))  ,RooFit.Components('gPDF_MC_lbtkbarDist_antilbtkMC'             ),RooFit.LineStyle(5 ),RooFit.LineColor(2) )

        plotframe.GetXaxis().SetTitle('J/#psi #bar{p} K^{+} Mass(GeV)')
        plotframe.Draw()
        plotContent=[
            ['combBkg_{0}'.format(label) ,'combinatorial background',],
            ['BdBkg_{0}'.format(label)   ,'B^{0}_{d} candidate',],
            ['bDBkg_{0}'.format(label)   ,'#bar{B}^{0}_{d} candidate',],
            ['LbSig_{0}'.format(label)   ,'#bar{#Lambda}^{0}_{b} candidate',],
            ]

        #canv.SaveAs(outFig)
        #figDir.cd()
        #plotframe.Draw()
        #plotframe.Write(label)

        #fitDir.cd()
        #fitres.Write(label)
        SaveResult(
                origPlot=plotframe,
                origVar=massBs,
                data={'content':binData, 'range':'sigRange'},
                totPDF={'content':myPDF, 'range':'sigRange'},
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )
    # fit 2016 data in Lb mass window end }}}


    print totNum
canv.SaveAs(outFig+']')
print 'jjj ee2'
outFile.cd()
space.Write()
outFile.Close()
print 'Bd dataset entries() = {0}, in signal region {1}'.format(loadDatasetBd.sumEntries(),loadDatasetBd.reduce('bdMass>5.1&&bdMass<5.5').sumEntries())
print 'bD dataset entries() = {0}, in signal region {1}'.format(loadDatasetbD.sumEntries(),loadDatasetbD.reduce('bdbarMass>5.1&&bdbarMass<5.5').sumEntries())

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

    myFrame.Draw()
    canv.SaveAs(outFig)
    # fit bdMass in BdToJpsiKstar892 MC end }}}
