#!/usr/bin/env python
# fit LbL0, LbLo in data and MC.
# use MC shape to determine the number in data.
# finalize Lambda0 cut for better fitting result.

from ROOT import TLegend
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService
import os


dataFile='result_flatNtuple_LbL0_preSelection_noKinematicCut.root'
outFileName='store_root/workspace_0thStep_LbL0Shape_noKinematicCut.{0}.root'.format(ptRange)
outFig='store_fig/pdf_workspace_0thStep_LbL0Shape_noKinematicCut.{0}.pdf'.format(ptRange)
#outFileName='workspace_0thStep_LbL0Shape_noKinematicCut.{0}.root'.format(ptRange)
#outFig='pdf_workspace_0thStep_LbL0Shape_noKinematicCut.{0}.pdf'.format(ptRange)

testMode=False

outFile=TFile('tmpLbL0.root','recreate')
pfigDir=outFile.mkdir('figs_pLbL0')
nfigDir=outFile.mkdir('figs_nLbL0')
figDir=outFile.mkdir('figs')
fitDir=outFile.mkdir('fitRes')

fitToLbMass_LbL0MC=True
fitToLbMass_LbLoMC=True
tMPfIG='tmpLbL0.pdf'

constredNames={'pLbL0':[], 'nLbL0':[]}
def createLegend(plotframe, contentList):
    leg=TLegend(0.60,0.70,0.89,0.89)
    for content in contentList:
        leg.AddEntry(plotframe.findObject(content[0]),content[1],'l')
    leg.SetFillColor(0)
    #leg.SetFillStyle(4000)
    leg.SetBorderSize(0)
    return leg
def SetMyRanges(myVar, nErr):
    mean=myVar.getVal()
    errs=myVar.getError()
    myVar.setRange(mean-nErr*errs, mean+nErr*errs)
    return None
def ConstraintVar(space, idxName, var):
    space.factory('Gaussian::{0}_Constr({0},{1},{2})'.format(var.GetName(),var.getVal(),var.getError()))
    constredNames[idxName].append( '{0}_Constr'.format(var.GetName()) )
    return space.pdf( '{0}_Constr'.format(var.GetName()) )
def ConstantVar(space, idxName, var):
    var.setConstant(True)
    #space.factory('Gaussian::{0}_Constr({0},{1},{2})'.format(var.GetName(),var.getVal(),var.getError()))
    #constredNames[idxName].append( '{0}_Constr'.format(var.GetName()) )
    #return space.pdf( '{0}_Constr'.format(var.GetName()) )
def SaveResult(**kwargs):
    print '------SaveResult start {0}'.format(label)
    plotframe=kwargs['origPlot']
    var=kwargs['origVar']
    data=kwargs['data']
    tPDF=kwargs['totPDF']
    kwargs['fitDir'].cd()
    kwargs['fitres'].Write(kwargs['label'])

    kwargs['figDir'].cd()
    plotframe.SetMaximum(plotframe.GetMaximum()*1.5)
    plotframe.Draw()
    plotframe.Write(kwargs['label'])
    canv.SaveAs(tMPfIG)

    #plotframeForPull=RooPlot(plotframe.GetXaxis().GetXmin(),plotframe.GetXaxis().GetXmax())
    plotframeForPull=var.frame(RooFit.Title(kwargs['label']+' creates for pull distribution'),RooFit.Range(plotframe.GetXaxis().GetXmin(),plotframe.GetXaxis().GetXmax()))
    #plotframeForPull.addPlotable(cutData,'p')
    data['content'].plotOn(plotframeForPull,RooFit.Name('data'))
    if not 'absNumNormalize' in kwargs.keys():
        tPDF['content'].plotOn(plotframeForPull,RooFit.Name('totModel'))
    else:
        tPDF['content'].plotOn(plotframeForPull,RooFit.Name('totModel'),RooFit.Normalization(kwargs['absNumNormalize'],RooAbsReal.NumEvent))
    #plotframeForPull.Draw()
    plotframeForPull.Write(label+'ForPull')
    print '------SaveResult End {0}'.format(label)
    return None

inF=TFile.Open(dataFile)
canv=TCanvas('c1','c1',1000,1000)
canv.SetFillColor(4000)
canv.SetFillStyle(4000)
canv.SaveAs('tmpLbL0.pdf'+'[')
TGaxis.SetMaxDigits(3)


space=RooWorkspace('space',False)
space.factory('lbl0Mass[5.4,5.9]')
space.factory('tktkMass[0.5,2.0]')
space.factory('lbl0Pt[0.,200.]')



space.factory('data_MC_factor[0.87]')
# fit lbl0Mass in LbL0 MC {{{
if fitToLbMass_LbL0MC:
    fitLabel='lbl0Dist_lbl0MC'
    mass=space.var('lbl0Mass')
    mass.setRange(fitLabel,5.5,5.75)


    inN=inF.Get('pLbL0/LbL0')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))


    # create target PDF.
    space.factory('mean_{0}[5.618,5.4,5.8]'.format(fitLabel))
    space.factory('Gaussian::gPDF_MCfit_{0}1(lbl0Mass,mean_{0},sigma_MCfit_{0}1[0.001,0.0001,1.0])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MCfit_{0}2(lbl0Mass,mean_{0},sigma_MCfit_{0}2[0.1,  0.0001,1.0])'.format(fitLabel))
    space.factory('SUM::gPDF_MCfit_{0}(frac1_{0}[0.8,0.5,1.0]*gPDF_MCfit_{0}1,gPDF_MCfit_{0}2)'.format(fitLabel))

    myPDF=space.pdf('gPDF_MCfit_{0}'.format(fitLabel))

    if testMode:
        fitres=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(False),RooFit.Save(False))
    else:
        fitres=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(True),RooFit.Save())



    space.factory('Product::sigma_%s1({data_MC_factor,sigma_MCfit_%s1})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s2({data_MC_factor,sigma_MCfit_%s2})' % (fitLabel,fitLabel))
    space.factory('Gaussian::gPDF_{0}1(lbl0Mass,mean_{0},sigma_{0}1)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}2(lbl0Mass,mean_{0},sigma_{0}2)'.format(fitLabel))
    space.factory('SUM::gPDF_{0}(frac1_{0}*gPDF_{0}1,gPDF_{0}2)'.format(fitLabel))
    #space.factory('SUM::gPDF_{0}(gPDF_{0}2)'.format(fitLabel))

    #ConstraintVar( space, 'pLbL0', space.var('mean_{0}'.format(fitLabel)) )
    #ConstraintVar( space, 'pLbL0', space.var('sigma_MCfit_{0}1'.format(fitLabel)) )
    #ConstraintVar( space, 'pLbL0', space.var('sigma_MCfit_{0}2'.format(fitLabel)) )
    #ConstraintVar( space, 'pLbL0', space.var('frac1_{0}'.format(fitLabel)) )
    ConstantVar( space, 'pLbL0', space.var('mean_{0}'.format(fitLabel)) )
    ConstantVar( space, 'pLbL0', space.var('sigma_MCfit_{0}1'.format(fitLabel)) )
    ConstantVar( space, 'pLbL0', space.var('sigma_MCfit_{0}2'.format(fitLabel)) )
    ConstantVar( space, 'pLbL0', space.var('frac1_{0}'.format(fitLabel)) )


    myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} #pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2),RooFit.LineWidth(1))

    myFrame.Draw()
    canv.SaveAs('tmpLbL0.pdf')
    pfigDir.cd()
    myFrame.Write(fitLabel)
    outFile.cd()
    fitres.Write(fitLabel)
    # fit lbl0Mass in Lb MC end }}}

# fit lbloMass in LbLo MC {{{
if fitToLbMass_LbLoMC:
    fitLabel='lbloDist_lbloMC'
    mass=space.var('lbl0Mass')
    mass.setRange(fitLabel,5.5,5.75)
    mass.setBins(50)


    inN=inF.Get('nLbL0/LbLo')
    dataset=RooDataSet('dataset','dataset',inN,RooArgSet(mass))


    # create target PDF.
    space.factory('mean_{0}[5.618,5.4,5.8]'.format(fitLabel))
    space.factory('Gaussian::gPDF_MCfit_{0}1(lbl0Mass,mean_{0},sigma_MCfit_{0}1[0.001,0.0001,1.0])'.format(fitLabel))
    space.factory('Gaussian::gPDF_MCfit_{0}2(lbl0Mass,mean_{0},sigma_MCfit_{0}2[0.1,  0.0001,1.0])'.format(fitLabel))
    space.factory('SUM::gPDF_MCfit_{0}(frac1_{0}[0.8,0.5,1.0]*gPDF_MCfit_{0}1,gPDF_MCfit_{0}2)'.format(fitLabel))

    myPDF=space.pdf('gPDF_MCfit_{0}'.format(fitLabel))

    if testMode:
        fitres=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(False),RooFit.Save(True))
    else:
        fitres=myPDF.fitTo(dataset,RooFit.Range(fitLabel),RooFit.Minos(True),RooFit.Save(True))



    space.factory('data_MC_factor_{0}[1.0,0.01,3.0]'.format(fitLabel))
    space.factory('Product::sigma_%s1({data_MC_factor,sigma_MCfit_%s1})' % (fitLabel,fitLabel))
    space.factory('Product::sigma_%s2({data_MC_factor,sigma_MCfit_%s2})' % (fitLabel,fitLabel))
    space.factory('Gaussian::gPDF_{0}1(lbl0Mass,mean_{0},sigma_{0}1)'.format(fitLabel))
    space.factory('Gaussian::gPDF_{0}2(lbl0Mass,mean_{0},sigma_{0}2)'.format(fitLabel))
    space.factory('SUM::gPDF_{0}(frac1_{0}*gPDF_{0}1,gPDF_{0}2)'.format(fitLabel))
    #space.factory('SUM::gPDF_{0}(gPDF_{0}1)'.format(fitLabel))

    #ConstraintVar( space, 'nLbL0', space.var('mean_{0}'.format(fitLabel)) )
    #ConstraintVar( space, 'nLbL0', space.var('sigma_MCfit_{0}1'.format(fitLabel)) )
    #ConstraintVar( space, 'nLbL0', space.var('sigma_MCfit_{0}2'.format(fitLabel)) )
    #ConstraintVar( space, 'nLbL0', space.var('frac1_{0}'.format(fitLabel)) )
    ConstantVar( space, 'nLbL0', space.var('mean_{0}'.format(fitLabel)) )
    ConstantVar( space, 'nLbL0', space.var('sigma_MCfit_{0}1'.format(fitLabel)) )
    ConstantVar( space, 'nLbL0', space.var('sigma_MCfit_{0}2'.format(fitLabel)) )
    ConstantVar( space, 'nLbL0', space.var('frac1_{0}'.format(fitLabel)) )

    #myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame=mass.frame(RooFit.Title(fitLabel))
    myFrame.GetXaxis().SetTitle('J/#psi #bar{p} #pi^{+} Mass(GeV)')
    dataset.plotOn(myFrame)
    myPDF.plotOn(myFrame,RooFit.LineColor(2),RooFit.LineWidth(1))

    myFrame.Draw()
    canv.SaveAs('tmpLbL0.pdf')
    nfigDir.cd()
    myFrame.Write(fitLabel)
    outFile.cd()
    fitres.Write(fitLabel)
    # fit lbloMass in lB MC end }}}
inF.Close()

load2016Data=True
if load2016Data:
    veryShortRangeFitLb=True
    veryShortRangeFitlB=True
    inFile16=TFile.Open('result_flatNtuple_LbL0_preSelection_noKinematicCut.root')
    inN16=inFile16.Get('pLbL0/2016Data')
    inn16=inFile16.Get('nLbL0/2016Data')

    massLb=space.var('lbl0Mass')
    massTkTk=space.var('tktkMass')

    massLb.setBins(50)

    loadDatasetLb=RooDataSet('loadData16p','loadData16',inN16,RooArgSet(massLb,massTkTk,space.var('lbl0Pt'))).reduce(ptCut)
    loadDatasetlB=RooDataSet('loadData16n','loadData16',inn16,RooArgSet(massLb,massTkTk,space.var('lbl0Pt'))).reduce(ptCut)
    totNum=inN16.GetEntries()
    space.factory('numLb[{0},-100.,{1}]'.format(50,totNum))
    space.factory('numlB[{0},-100.,{1}]'.format(50,totNum))



    #tktkMassCut='tktkMass>1.100&&tktkMass<1.120'
    tktkMassCut='tktkMass>1.105&&tktkMass<1.125'
    #tktkMassCut='tktkMass>1.110&&tktkMass<1.120'
    # fit 2016 data in short range Lb mass window LbL0 {{{
    if veryShortRangeFitLb:
        massLb.setRange('sigShortRange',5.4,5.9)
        massLb.setBins(50)
        #binData=loadDatasetLb.binnedClone('shortBinLb')
        binData=loadDatasetLb.reduce(tktkMassCut)

        label='Run2016Data_pLbL0'
        fitLabel='lbl0Dist_lbl0MC'
        space.factory('x0[-5.498]')
        space.factory('Addition::X({{ {x},x0 }})'.format(x='lbl0Mass'))
        space.factory('Polynomial::pPDF_%s(X,{c1_%s[0.01,-2.,2.],c2_%s[0.01,-3.,3.0],c3_%s[0.01,-1.,3.]})' % (label,label,label,label) )
        #space.factory('Polynomial::pPDF_%s(lbl0Mass,{c1_%s[0.01,-5.,5.]})' % (label,label) )

        # set resolution issue: Convolute a gaussian.
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label, totNum,totNum))
        myPDF=RooAddPdf('totPdf_{0}'.format(label),'totPdf_{0}'.format(label),
                RooArgList( space.pdf('pPDF_{0}'.format(label)),
                            space.pdf('gPDF_lbl0Dist_lbl0MC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numLb') ),
                False)
        getattr(space,'import')(myPDF)

        constrSet=RooArgSet()
        for constredName in constredNames['pLbL0']:
            constrSet.add(space.pdf(constredName))


        fitres=myPDF.fitTo(binData,RooFit.Range('sigShortRange'),RooFit.Save(),RooFit.Minos(True),RooFit.ExternalConstraints(constrSet))
        #fitres=myPDF.fitTo(binData,RooFit.Range('sigShortRange'),RooFit.Save(),RooFit.Minos(True))

        plotframe=massLb.frame(RooFit.Title(label),RooFit.Range('sigShortRange'))
        binData.plotOn(plotframe,RooFit.Name('data'))
        myPDF.plotOn(plotframe,RooFit.Name('totModel'),RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Name('combBkg'),RooFit.Components('pPDF_{0}'            .format(label)),RooFit.LineWidth(1),RooFit.LineColor(27))
        myPDF.plotOn(plotframe,RooFit.Name('sig')  ,RooFit.Components('gPDF_lbl0Dist_lbl0MC'              ),RooFit.LineStyle(5),RooFit.LineColor(8 ))


        plotframe.Draw()
        #canv.SaveAs('tmpLbL0.pdf')
        #pfigDir.cd()
        #plotframe.Write(label)
        #outFile.cd()
        #fitres.Write(label)
        SaveResult(
                origPlot=plotframe,
                origVar=massLb,
                data={'content':binData},
                totPDF={'content':myPDF},
                fitres=fitres,
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )
    # fit 2016 data in Lb mass window end }}}
    # fit 2016 data in short range Lb mass window LbLo {{{
    if veryShortRangeFitlB:
        massLb.setRange('sigShortRange',5.4,5.9)
        massLb.setBins(50)
        #binData=loadDatasetLb.binnedClone('shortBinLb')
        binData=loadDatasetlB.reduce(tktkMassCut)

        label='Run2016Data_nLbL0'
        fitLabel='lbloDist_lbloMC'
        space.factory('Polynomial::pPDF_%s(X,{c1_%s[0.01,-2.,2.],c2_%s[0.01,-3.,3.0],c3_%s[0.01,-1.,3.]})' % (label,label,label,label) )

        # set resolution issue: Convolute a gaussian.
        space.factory('numCombBkg_{0}[{1},0.,{2}]'.format(label, totNum,totNum))
        myPDF=RooAddPdf('totPdf_{0}'.format(label),'totPdf_{0}'.format(label),
                RooArgList( space.pdf('pPDF_{0}'.format(label)),
                            space.pdf('gPDF_lbloDist_lbloMC') ),
                RooArgList( space.var('numCombBkg_{0}'.format(label)),
                            space.var('numlB') ),
                False)
        getattr(space,'import')(myPDF)

        constrSet=RooArgSet()
        for constredName in constredNames['nLbL0']:
            constrSet.add(space.pdf(constredName))

        fitres=myPDF.fitTo(binData,RooFit.Range('sigShortRange'),RooFit.Save(),RooFit.Minos(True),RooFit.ExternalConstraints(constrSet))

        plotframe=massLb.frame(RooFit.Title(label),RooFit.Range('sigShortRange'))
        binData.plotOn(plotframe,RooFit.Name('data'))
        myPDF.plotOn(plotframe,RooFit.Name('totModel'),RooFit.LineWidth(1),RooFit.LineColor(2))
        myPDF.plotOn(plotframe,RooFit.Name('combBkg'),RooFit.Components('pPDF_{0}'            .format(label)),RooFit.LineWidth(1),RooFit.LineColor(27))
        myPDF.plotOn(plotframe,RooFit.Name('sig')  ,RooFit.Components('gPDF_lbloDist_lbloMC'              ),RooFit.LineStyle(5 ),RooFit.LineColor(8))

        plotframe.Draw()
        #canv.SaveAs('tmpLbL0.pdf')
        #nfigDir.cd()
        #plotframe.Write(label)
        #outFile.cd()
        #fitres.Write(label)
        SaveResult(
                origPlot=plotframe,
                origVar=massLb,
                data={'content':binData},
                totPDF={'content':myPDF},
                fitres=fitres,
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )
    # fit 2016 data in Lb mass window end }}}

    if not testMode:
        outFile.cd()
        space.Write()
        outFile.Close()
canv.SaveAs('tmpLbL0.pdf'+']')
os.system('mv tmpLbL0.pdf {0}'.format(outFig))
os.system('mv tmpLbL0.root {0}'.format(outFileName))
