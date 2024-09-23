#!/usr/bin/env python
# 1. fit Bd shape by Bd signal + bkg components: bD, Bs, double exp
# 2. fit bD shape by bD signal + bkg components: Bd, Bs, double exp
# 3. simultaneous fit to Bd and bD to get certain yield of Bd and bD.
# 4. fit Bs shape by Bs signal + bkg components: Bd, bD, double exp, fix the yield result from simultaneous fit
# 5. use data driven clean signals to check yield result is true or not in previous fit.

# 6. fit Lb signal region. This is final version: only basic kinematic cut (loose cut).
#    and the background is only 2nd order polynomial.

import os
from array import array
from ROOT import TLegend, TBox, TLine
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis, TPad, TLine, TGraphErrors, TRatioPlot, TGraph, gRandom, TNtupleD
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsData, RooPlot, RooAbsReal, RooExtendPdf
import time


#dataFileName='result_flatNtuple_NoSelection.root'

dataFileName='store_root/result_flatNtuple_LbTk_preSelection_noKinematicCut.root'
storeFileName='store_root/workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.{0}.root'.format(ptRange)
storeFigName='store_fig/pdf_workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.{0}.pdf'.format(ptRange)
#dataFileName='store_root/result_flatNtuple_LbTk_preSelection_withKinematicCut.root'
#storeFileName='store_root/workspace_extraStep_1st_shortRangeLbFit_withKinematicCut.root'
#storeFigName='store_fig/pdf_workspace_extraStep_1st_shortRangeLbFit_withKinematicCut.pdf'

tMPrOOTnAME='tmp.root'
tMPfIG='tmp.pdf'
txtRecFile=open('log_timeRec.txt','w')
currenttime=time.time()
rectime=currenttime
txtRecFile.write('start run job')
def recTime(mesg):
    global currenttime
    rectime=currenttime
    currenttime=time.time()
    txtRecFile.write('{0} in {1} minutes\n'.format(mesg,int((currenttime-rectime)/60)))


outFile=TFile(tMPrOOTnAME,'recreate')
figDir=outFile.mkdir('figs')
fitDir=outFile.mkdir('fitRes')
ColorSetup={
        'Lb':{'color': 8,'style':2},
        'lB':{'color':30,'style':2},
        'Bd':{'color': 9,'style':4},
        'bD':{'color':40,'style':4},
        'Bs':{'color':42,'style':7},
        'comb':{'color':13,'style':5},
        #'LbL0':{'color':30,'style':8},
        #'lBLo':{'color':31,'style':8},
        }


# set output message level
RooMsgService.instance().setGlobalKillBelow(4)

useMinos=True
allowedNum=5.

def NewCanvas(name='c1'):
    canv=TCanvas(name,'',1000,1000)
    canv.SetFillColor(4000)
    canv.SetFillStyle(4000)
    return canv
canv=NewCanvas()
canv.SaveAs(tMPfIG+'[')
TGaxis.SetMaxDigits(3)

recTime('start-def func')

# def functions {{{
def SaveSimulResult(**kwargs):
    print '------SaveSimulResult start {0}'.format(kwargs['label'])
    plotframes=kwargs['origPlot']
    vars=kwargs['origVar']
    datas=kwargs['data']
    tPDFs=kwargs['totPDF']
    label=kwargs['label']
    kwargs['fitDir'].cd()
    kwargs['fitres'].Write(kwargs['label'])

    for idx,plotframe in enumerate(plotframes):
        var=vars[idx]
        data=datas[idx]
        tPDF=tPDFs[idx]
        frameName=plotframe.GetName()

        kwargs['figDir'].cd()
        plotframe.SetMaximum(plotframe.GetMaximum()*1.5)
        plotframe.Draw()
        canv.SaveAs(tMPfIG)
        plotframe.Write(label+'In'+plotframe.GetName())

        plotframeForPull=var.frame(RooFit.Title(label+' creates for pull distribution'+'in {0} frame'.format(frameName)),RooFit.Range(plotframe.GetXaxis().GetXmin(),plotframe.GetXaxis().GetXmax()))
        data['content'].plotOn(plotframeForPull,RooFit.Name('data'))
        tPDF['content'].plotOn(plotframeForPull,RooFit.Name('totModel'))
        plotframeForPull.Write(label+'ForPull'+'_{0}Frame'.format(frameName))
    print '------SaveSimulResult End {0}'.format(kwargs['label'])
    return None
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

def CheckToyMC(space,pdf,var,snapshot):
    toyData=pdf.generate(RooArgSet(var),100000)
    fitres=pdf.fitTo(toyData,RooFit.Save(True))

    frame=var.frame(RooFit.Title('ToyMC check in {0}'.format(var.GetName())))
    toyData.plotOn(frame, RooFit.Name('toydata'))
    pdf.plotOn(frame, RooFit.Name('totpdf'),RooFit.Normalization( toyData.sumEntries(),RooAbsReal.NumEvent))
    frame.Draw()

    SaveResult(
            origPlot=frame,
            origVar=var,
            data={'content':toyData},
            totPDF={'content':pdf},
            fitres=fitres,
            label='ToyMCcheck_{0}'.format(var.GetName()),
            fitDir=fitDir,
            figDir=figDir,
            )
    #space.loadSnapshot(snapshot)
    return None
# def functions end }}}

recTime('def funcs')
space=RooWorkspace('space',False)

# new parameters
space.factory('bsMass[5.25,5.50]')
space.factory('bdMass[5.10,5.50]')
space.factory('bdbarMass[5.10,5.50]')
space.factory('lbtkMass   [5.4,5.9]')
space.factory('lbtkbarMass[5.4,5.9]')
space.factory('lbtkPt[0.,200.]')

space.factory('kkMass[0.8,10.0]')
space.factory('kpiMass[0.8,10.0]')
space.factory('kpibarMass[0.8,10.0]')


########## load workspace ####################
workspaceFile1=TFile.Open('store_root/workspace_1stStep_MCShape.root')
space1st=workspaceFile1.Get('space')
space1st.SetName('space1st')
workspaceFile2=TFile.Open('store_root/workspace_2ndStep_dataFit.root')
space2nd=workspaceFile2.Get('space')
space2nd.SetName('space2nd')


load2016Data=True
if load2016Data:
    BdModelBuilding=False
    bDModelBuilding=False
    BsModelBuilding=False
    directsimBdFitData=False

    checkRawBsData=False
    checkRawData=False


    LbModelBuilding=True
    lBModelBuilding=True
    directsimLbFitData=False

    scanLikelihoodLb=False

    LbStabilityFit=False

    inFile16=TFile.Open(dataFileName)
    #inN16=inFile16.Get('2016Data')
    inN16=inFile16.Get('pLbTk/2016Data')
    inn16=inFile16.Get('nLbTk/2016Data')

    # load parameters from other workspace and import them in current workspace
    massLb=space.var('lbtkMass')
    masslB=space.var('lbtkbarMass')
    massBs=space.var('bsMass')
    #massBd=space.var('bdMass')
    #massbD=space.var('bdbarMass')


    massLb.setBins(50)
    masslB.setBins(50)
    #massBd.setBins(80)
    #massbD.setBins(80)
    massBs.setBins(50)

    massLb.setRange('sigRangeLb',5.4,5.9)
    masslB.setRange('sigRangelB',5.4,5.9)
    #massBd.setRange('sigRangeBd',5.1,5.5)
    #massbD.setRange('sigRangebD',5.1,5.5)

    loadDatasetBs=RooDataSet('loadDatasetBs','loadData16',inN16,RooArgSet(massBs,space.var('kkMass')))
    #loadDatasetBd=RooDataSet('loadDatasetBd','loadData16',inN16,RooArgSet(massBd,space.var('kpiMass')))
    #loadDatasetbD=RooDataSet('loadDatasetbD','loadData16',inN16,RooArgSet(massbD,space.var('kpibarMass')))
    loadDatasetLb=RooDataSet('loadDatasetLb','loadData16',inN16,RooArgSet(massLb,space.var('lbtkPt')))
    loadDatasetlB=RooDataSet('loadDatasetlB','loadData16',inn16,RooArgSet(masslB,space.var('lbtkPt')))
    totNum=loadDatasetLb.sumEntries()
    space.factory('numLb[{0},-1000.,{1}]'.format(space2nd.var('numLb').getVal(),totNum))
    #space.factory('numlB[{0},0.,{1}]'.format(space2nd.var('numlB').getVal(),totNum))
    space.factory('numlB[{0},-1000.,{1}]'.format(2000.,totNum))
    space.factory('numBs[{0},0.,{1}]'.format(space2nd.var('numBs').getVal(),totNum))
    #space.factory('numBd[{0},0.,{1}]'.format(space2nd.var('numBd').getVal(),totNum))
    #space.factory('numbD[{0},0.,{1}]'.format(space2nd.var('numbD').getVal(),totNum))

    ## used in LbMass
    #space.factory('kPDF_Lbfactor_BdNum[{fracVal}]'.format(fracVal=(space2nd.var('kPDF_Lbfactor_BdNum').getVal())))
    #space.factory('kPDF_Lbfactor_bDNum[{fracVal}]'.format(fracVal=(space2nd.var('kPDF_Lbfactor_bDNum').getVal())))
    #space.factory('kPDF_Lbfactor_BsNum[{fracVal}]'.format(fracVal=(space2nd.var('kPDF_Lbfactor_BsNum').getVal())))
    #space.factory('Product::fracBdNum_inLbDist({kPDF_Lbfactor_BdNum,numBd})')
    #space.factory('Product::fracbDNum_inLbDist({kPDF_Lbfactor_bDNum,numbD})')
    #space.factory('Product::fracBsNum_inLbDist({kPDF_Lbfactor_BsNum,numBs})')

    ## used in BdMass
    #space.factory('kPDF_Bdfactor_bDNum[{fracVal}]'.format(fracVal=(space2nd.var('kPDF_Bdfactor_bDNum').getVal())))
    #space.factory('kPDF_Bdfactor_BsNum[{fracVal}]'.format(fracVal=(space2nd.var('kPDF_Bdfactor_BsNum').getVal())))
    #space.factory('Product::fracBsNum_inBdDist({kPDF_Bdfactor_BsNum,numBs})')
    #space.factory('Product::fracbDNum_inBdDist({kPDF_Bdfactor_bDNum,numbD})')

    ## used in bDMass
    #space.factory('kPDF_bDfactor_BdNum[{fracVal}]'.format(fracVal=(space2nd.var('kPDF_bDfactor_BdNum').getVal())))
    #space.factory('kPDF_bDfactor_BsNum[{fracVal}]'.format(fracVal=(space2nd.var('kPDF_bDfactor_BsNum').getVal())))
    #space.factory('Product::fracBsNum_inbDDist({kPDF_bDfactor_BsNum,numBs})')
    #space.factory('Product::fracBdNum_inbDDist({kPDF_bDfactor_BdNum,numBd})')

    simulComponents=[]


    recTime('xxxxxxxxx')
    # build Bd Model {{{
    if BdModelBuilding:
        label='BdModel'
        print '--- Block start to build {0} ---'.format(label)

        testKeyPdf=False
        buildSigModel=True
        buildBKGModel=True
        performTotalFit=True
        mcLabel='bdDist_BdK892MC'
        fitLabel='BdBKG'
        ePDFsList=[]
        varName='bdMass'
        fitRange='sigRangeBd'
        dataset=loadDatasetBd

        if buildSigModel:
            print '--- Block start to build Sig Model in section [{0}] ---'.format(label)
            mcMean  =space1st.var('mu_{0}'.format(mcLabel))
            mcSigma1=space2nd.var('sig_{0}1'.format(mcLabel))
            mcSigma2=space2nd.var('sig_{0}2'.format(mcLabel))
            mcFrac1 =space2nd.var('gPDF_frac1_{0}'.format(mcLabel))
            numTag='numBd'
            mcNum   =space2nd.var(numTag)
            mcMean  .setConstant(False)
            mcSigma1.setConstant(False)
            mcSigma2.setConstant(False)
            mcFrac1 .setConstant(False)

            # rooworkspace version
            getattr(space,'import')(space1st.var('mu_{0}'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('sig_{0}1'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('sig_{0}2'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('gPDF_frac1_{0}'.format(mcLabel)))
            space.factory('Gaussian::gPartPDF_{label}1({massVar},mu_{label},sig_{label}1)'.format(massVar=varName,label=mcLabel))
            space.factory('Gaussian::gPartPDF_{label}2({massVar},mu_{label},sig_{label}2)'.format(massVar=varName,label=mcLabel))
            space.factory('SUM::gPDF_{llabel}(gPDF_frac1_{label}*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,llabel=fitLabel))
            space.factory('ExtendPdf::eSigModel_{llabel}(gPDF_{llabel},{num})'.format(llabel=fitLabel,num=numTag))

            ePDFsList.append({'tag':'Bd','name':'eSigModel_{llabel}'.format(llabel=fitLabel)})
            print '--- Block ending to build Sig Model in section [{0}] ---'.format(label)
        else:
            print '--- Block start  to build Sig Model in section [{0}] sideband only!---'.format(label)
            mass=space.var(varName).setRange('Lside',5.1,5.22)
            mass=space.var(varName).setRange('Rside',5.34,6.0)
            fitRange=[]
            fitRange.append('Lside')
            fitRange.append('Rside')
            print '--- Block ending to build Sig Model in section [{0}] sideband only!---'.format(label)



        if buildBKGModel:
            print '--- Block start to build Bkg Model in section [{0}] ---'.format(label)
            # build rooworkspace version
            # build particles background
            nameBkgs=[{'tag':'bD','name':'kPDF_bdDist_antiBdK892MC'},{'tag':'Bs','name':'kPDF_bdDist_BsFMC'}]
            numBkgNames=['fracbDNum_inBdDist','fracBsNum_inBdDist']

            for idx,bkg in enumerate(nameBkgs):
                print 'idx = {0}, name = {1}'.format(idx,bkg['name'])
                getattr(space,'import')(space2nd.pdf(bkg['name']))
                space.factory('ExtendPdf::eBkgModel_{label}({pdf},{num})'.format(label=bkg['name'],pdf=bkg['name'],num=numBkgNames[idx]))
                ePDFsList.append({'tag':bkg['tag'],'name':'eBkgModel_{llabel}'.format(llabel=bkg['name'])})
            # bulid combinatorial background
            nameComb='cPDF_{0}'.format(fitLabel)
            numCombName='numCombBkg_{0}'.format(fitLabel)
            loadNumComb=space2nd.var(numCombName)
            getattr(space,'import')(space2nd.var('cPar_{0}1'.format(fitLabel)))
            getattr(space,'import')(space2nd.var('cPar_{0}2'.format(fitLabel)))
            getattr(space,'import')(space2nd.var('mShift_{0}'.format(fitLabel)))

            space.factory('{name}[{initVal},{minVal},{maxVal}]'.format(name=numCombName,
                initVal=loadNumComb.getVal(),minVal=loadNumComb.getMin(),maxVal=loadNumComb.getMax()))
            space.factory('EXPR::{name}("{x}>mShift_{label}?( exp(-1.*({x}-mShift_{label})/(cPar_{label}1+cPar_{label}2)) - exp(-1.*({x}-mShift_{label})/cPar_{label}1) ):0.",{x},mShift_{label},cPar_{label}1,cPar_{label}2)'.format(name=nameComb,label=fitLabel,x=varName))
            space.factory('ExtendPdf::e{name}({pdf},{num})'.format(name=nameComb,pdf=nameComb,num=numCombName))
            ePDFsList.append({'tag':'comb','name':'e'+nameComb})
            print '--- Block ending to build Bkg Model in section [{0}] ---'.format(label)




        # build total model and fit
        if buildBKGModel:
            print '--- Block start to build Tot Model in section [{0}] ---'.format(label)
            if testKeyPdf:
                ultraPurebDSelection='bdbarMass>5.15&&bdbarMass<5.4&&kpibarMass>0.86&&kpibarMass<0.92 && !(bdMass>5.25&&bdMass<5.32&&bdbarMass>5.25&&bdbarMass<5.32)'
                hist=TH1D("ultraPureBd",'ultraPureBd',185,5.15,7.0)
                inN16.Draw('bdMass>>ultraPureBd',ultraPurebDSelection)
                bindata=RooDataHist('bindata','bindata',RooArgList(massBd),hist)

                sigPdf=space.pdf('kPDF_bdDist_antiBdK892MC')
                space.factory('kNum[{0},0.,{1}]'.format(hist.GetEntries()-2567.,hist.GetEntries()*2.))
                space.factory('ExtendPdf::purebDinBdMass({pdf},{num})'.format(pdf='kPDF_bdDist_antiBdK892MC',num='kNum'))
                esigPdf=space.pdf('purebDinBdMass')
                esigPdf.fitTo(bindata,RooFit.Range('Lside,Rside'))
                frame=massBd.frame(RooFit.Title('ultra pure bD in massBd frame'))
                bindata.plotOn(frame)
                esigPdf.plotOn(frame,RooFit.LineColor(2),RooFit.LineStyle(2))
                frame.Draw()
                canv.SaveAs(tMPfIG)


            if checkRawData:
                pureBdSelection='bdMass>5.15&&bdMass<5.4&&kpiMass>0.85&&kpiMass<0.95'
                purebDSelection='bdbarMass>5.15&&bdbarMass<5.4&&kpibarMass>0.85&&kpibarMass<0.95'
                pureBsSelection='bsMass>5.3&&bsMass<5.5&&kkMass<1.03&&kkMass>1.01'
                pureData=loadDatasetBd.reduce(pureBdSelection)
                mass=massBd
                fitRange='dataDrivenBd'
                mass.setRange(fitRange,5.15,5.4)

                esig=space.pdf('eSigModel_BdBKG')
                ebkg1=space.pdf('eBkgModel_kPDF_bdDist_antiBdK892MC')

                c1Var=RooRealVar('c1','c1',0.02,-5.,5.)
                bkgPdf=RooPolynomial('bkgpdf','bkgpdf',mass,RooArgList(c1Var))
                numbkg=RooRealVar('numbkg','numbkg',200,0.,5000.)
                ebkg2=RooExtendPdf('ebkg','ebkg',bkgPdf,numbkg)
                tPdf=RooAddPdf('tot','tot',RooArgList(esig,ebkg1,ebkg2))

                fitRes=tPdf.fitTo(pureData,RooFit.Save(True),RooFit.Range(fitRange))

                xframe=mass.frame(RooFit.Range(fitRange),RooFit.Title(fitRange))
                pureData.plotOn(xframe,RooFit.Name('data'))
                tPdf.plotOn(xframe,RooFit.Name('totPdf'))
                tPdf.plotOn(xframe,RooFit.Name('sig1'),RooFit.Components('eSigModel_BdBKG'),RooFit.LineStyle(2),RooFit.LineColor(30))
                tPdf.plotOn(xframe,RooFit.Name('sig2'),RooFit.Components('eSigModel_kPDF_bdDist_antiBdK892MC'),RooFit.LineStyle(2),RooFit.LineColor(25))
                xframe.Draw()
                fitres=fitRes
                SaveResult(
                        origPlot=xframe,
                        origVar=mass,
                        data={'content':pureData},
                        totPDF={'content':tPdf},
                        fitres=fitres,
                        label=fitRange,
                        fitDir=fitDir,
                        figDir=figDir,
                        )
            mcMean  =space1st.var('mu_{0}'.format(mcLabel)).setConstant(True)
            mcSigma1=space2nd.var('sig_{0}1'.format(mcLabel)).setConstant(True)
            mcSigma2=space2nd.var('sig_{0}2'.format(mcLabel)).setConstant(True)
            mcFrac1 =space2nd.var('gPDF_frac1_{0}'.format(mcLabel)).setConstant(True)


            if performTotalFit:
                ePdfSet=RooArgList()
                for ePDF in ePDFsList:
                    ePdfSet.add(space.pdf(ePDF['name']))

                totPdf=RooAddPdf('totPdf_{0}'.format(label),'totPdf_{0}'.format(label),ePdfSet)
                if not buildSigModel:
                    fitRange=','.join(fitRange)
                fitRes=totPdf.fitTo(dataset.reduce('{x}>5.1&&{x}<5.5'.format(x=varName)),RooFit.Save(True),RooFit.Range(fitRange))


                xframe=space.var(varName).frame(RooFit.Title("load {0} Fit for check".format(varName)),RooFit.Range(fitRange))
                dataset.plotOn(xframe,RooFit.Name('data'))
                totPdf.plotOn(xframe, RooFit.Name('totModel'),RooFit.LineColor(2))
                for pdf in ePDFsList:
                    setup=ColorSetup[pdf['tag']]
                    totPdf.plotOn(xframe,RooFit.Name(pdf['tag']),RooFit.Components(pdf['name']),
                            RooFit.LineColor(setup['color']),RooFit.LineStyle(setup['style']),RooFit.LineWidth(4))

                xframe.Draw()
                fitres=fitRes
                SaveResult(
                        origPlot=xframe,
                        origVar=space.var(varName),
                        data={'content':dataset},
                        totPDF={'content':totPdf},
                        fitres=fitres,
                        label=label,
                        fitDir=fitDir,
                        figDir=figDir,
                        )
                simulComponents.append({'cat':'BdPart','pdf':totPdf,'components':ePDFsList})
            print '--- Block ending to build Tot Model in section [{0}] ---'.format(label)
    # build Bd model end }}}
    recTime('build Bd interval')
    # build bD Model {{{
    if bDModelBuilding:
        label='bDModel'
        print '--- Block start to build {0} ---'.format(label)

        buildSigModel=True
        buildBKGModel=True
        buildBdTotModelAndFit=True
        mcLabel='bdbarDist_antiBdK892MC'
        fitLabel='bDBKG'
        ePDFsList=[]
        dataset=loadDatasetbD

        if buildSigModel:
            print '--- Block start to build Sig Model in section [{0}] ---'.format(label)
            mcMean  =space1st.var('mu_{0}'.format(mcLabel))
            mcSigma1=space2nd.var('sig_{0}1'.format(mcLabel))
            mcSigma2=space2nd.var('sig_{0}2'.format(mcLabel))
            mcFrac1 =space2nd.var('gPDF_frac1_{0}'.format(mcLabel))
            numTag='numbD'
            varName='bdbarMass'
            mcNum   =space2nd.var(numTag)
            mcMean  .setConstant(True)
            mcSigma1.setConstant(True)
            mcSigma2.setConstant(True)
            mcFrac1 .setConstant(True)

            # rooworkspace version
            getattr(space,'import')(space1st.var('mu_{0}'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('sig_{0}1'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('sig_{0}2'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('gPDF_frac1_{0}'.format(mcLabel)))
            space.factory('Gaussian::gPartPDF_{label}1({massVar},mu_{label},sig_{label}1)'.format(massVar=varName,label=mcLabel))
            space.factory('Gaussian::gPartPDF_{label}2({massVar},mu_{label},sig_{label}2)'.format(massVar=varName,label=mcLabel))
            space.factory('SUM::gPDF_{llabel}(gPDF_frac1_{label}*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,llabel=fitLabel))
            space.factory('ExtendPdf::eSigModel_{llabel}(gPDF_{llabel},{num})'.format(llabel=fitLabel,num=numTag))

            ePDFsList.append({'tag':'bD','name':'eSigModel_{llabel}'.format(llabel=fitLabel)})
            print '--- Block ending to build Sig Model in section [{0}] ---'.format(label)


        if buildBKGModel:
            print '--- Block start to build Bkg Model in section [{0}] ---'.format(label)
            # build rooworkspace version
            # build particles background
            nameBkgs=[{'tag':'Bd','name':'kPDF_bdbarDist_BdK892MC'},{'tag':'Bs','name':'kPDF_bdbarDist_BsFMC'}]
            numBkgNames=['fracBdNum_inbDDist','fracBsNum_inbDDist']

            for idx,bkg in enumerate(nameBkgs):
                print 'idx = {0}, name = {1}'.format(idx,bkg['name'])
                getattr(space,'import')(space2nd.pdf(bkg['name']))
                space.factory('ExtendPdf::eBkgModel_{label}({pdf},{num})'.format(label=bkg['name'],pdf=bkg['name'],num=numBkgNames[idx]))
                ePDFsList.append({'tag':bkg['tag'],'name':'eBkgModel_{llabel}'.format(llabel=bkg['name'])})
            # bulid combinatorial background
            nameComb='cPDF_{0}'.format(fitLabel)
            numCombName='numCombBkg_{0}'.format(fitLabel)
            loadNumComb=space2nd.var(numCombName)
            getattr(space,'import')(space2nd.var('cPar_{0}1'.format(fitLabel)))
            getattr(space,'import')(space2nd.var('cPar_{0}2'.format(fitLabel)))
            getattr(space,'import')(space2nd.var('mShift_{0}'.format(fitLabel)))

            space.factory('{name}[{initVal},{minVal},{maxVal}]'.format(name=numCombName,
                initVal=loadNumComb.getVal(),minVal=loadNumComb.getMin(),maxVal=loadNumComb.getMax()))
            space.factory('EXPR::{name}("{x}>mShift_{label}?( exp(-1.*({x}-mShift_{label})/(cPar_{label}1+cPar_{label}2)) - exp(-1.*({x}-mShift_{label})/cPar_{label}1) ):0.",{x},mShift_{label},cPar_{label}1,cPar_{label}2)'.format(name=nameComb,label=fitLabel,x=varName))
            space.factory('ExtendPdf::e{name}({pdf},{num})'.format(name=nameComb,pdf=nameComb,num=numCombName))
            ePDFsList.append({'tag':'comb','name':'e'+nameComb})
            print '--- Block ending to build Bkg Model in section [{0}] ---'.format(label)




        if buildBdTotModelAndFit:
            print '--- Block start to build Tot Model in section [{0}] ---'.format(label)
            if checkRawData:
                pureBdSelection='bdMass>5.15&&bdMass<5.4&&kpiMass>0.85&&kpiMass<0.95'
                purebDSelection='bdbarMass>5.15&&bdbarMass<5.4&&kpibarMass>0.85&&kpibarMass<0.95'
                pureBsSelection='bsMass>5.3&&bsMass<5.5&&kkMass<1.03&&kkMass>1.01'
                pureData=loadDatasetbD.reduce(purebDSelection)
                mass=massbD
                fitRange='dataDrivenbD'
                mass.setRange(fitRange,5.15,5.4)

                esig=space.pdf('eSigModel_bDBKG')
                ebkg1=space.pdf('eBkgModel_kPDF_bdbarDist_BdK892MC')

                c1Var=RooRealVar('c1','c1',0.02,-5.,5.)
                bkgPdf=RooPolynomial('bkgpdf','bkgpdf',mass,RooArgList(c1Var))
                numbkg=RooRealVar('numbkg','numbkg',200,0.,5000.)
                ebkg2=RooExtendPdf('ebkg','ebkg',bkgPdf,numbkg)
                tPdf=RooAddPdf('tot','tot',RooArgList(esig,ebkg1,ebkg2))

                fitRes=tPdf.fitTo(pureData,RooFit.Save(True),RooFit.Range(fitRange))

                xframe=mass.frame(RooFit.Range(fitRange),RooFit.Title(fitRange))
                pureData.plotOn(xframe,RooFit.Name('data'))
                tPdf.plotOn(xframe,RooFit.Name('totPdf'))
                tPdf.plotOn(xframe,RooFit.Name('sig1'),RooFit.Components('eSigModel_bDBKG'),RooFit.LineStyle(2),RooFit.LineColor(30))
                tPdf.plotOn(xframe,RooFit.Name('sig2'),RooFit.Components('eSigModel_kPDF_bdbarDist_BdK892MC'),RooFit.LineStyle(2),RooFit.LineColor(25))
                xframe.Draw()
                fitres=fitRes
                SaveResult(
                        origPlot=xframe,
                        origVar=mass,
                        data={'content':pureData},
                        totPDF={'content':tPdf},
                        fitres=fitres,
                        label=fitRange,
                        fitDir=fitDir,
                        figDir=figDir,
                        )
            mcMean  =space1st.var('mu_{0}'.format(mcLabel)).setConstant(True)
            mcSigma1=space2nd.var('sig_{0}1'.format(mcLabel)).setConstant(True)
            mcSigma2=space2nd.var('sig_{0}2'.format(mcLabel)).setConstant(True)
            mcFrac1 =space2nd.var('gPDF_frac1_{0}'.format(mcLabel)).setConstant(True)

        if performTotalFit:
            ePdfSet=RooArgList()
            for ePDF in ePDFsList:
                ePdfSet.add(space.pdf(ePDF['name']))

            totPdf=RooAddPdf('totPdf_{0}'.format(label),'totPdf_{0}'.format(label),ePdfSet)
            fitRes=totPdf.fitTo(dataset.reduce('{x}>5.1&&{x}<5.5'.format(x=varName)),RooFit.Save(True))


            xframe=space.var(varName).frame(RooFit.Title("load {0} Fit for check".format(varName)))
            dataset.plotOn(xframe,RooFit.Name('data'))
            totPdf.plotOn(xframe, RooFit.Name('totModel'),RooFit.LineColor(2))
            for pdf in ePDFsList:
                setup=ColorSetup[pdf['tag']]
                totPdf.plotOn(xframe,RooFit.Name(pdf['tag']),RooFit.Components(pdf['name']),
                        RooFit.LineColor(setup['color']),RooFit.LineStyle(setup['style']),RooFit.LineWidth(4))

            xframe.Draw()
            fitres=fitRes
            SaveResult(
                    origPlot=xframe,
                    origVar=space.var(varName),
                    data={'content':dataset},
                    totPDF={'content':totPdf},
                    fitres=fitres,
                    label=label,
                    fitDir=fitDir,
                    figDir=figDir,
                    )
            simulComponents.append({'cat':'bDPart','pdf':totPdf,'components':ePDFsList})
            print '--- Block ending to build Tot Model in section [{0}] ---'.format(label)
    # build Bd model end }}}
    recTime('build bD interval')
    # build Bs Model {{{
    if BsModelBuilding:
        label='BsModel'
        print '--- Block start to build {0} ---'.format(label)

        buildSigModel=True
        buildBKGModel=True
        performTotalFit=True
        mcLabel='bsDist_BsFMC'
        fitLabel='BsBKG'
        ePDFsList=[]
        varName='bsMass'
        fitRange='sigRangeBs'
        dataset=loadDatasetBs

        if buildSigModel:
            print '--- Block start to build Sig Model in section [{0}] ---'.format(label)
            # rooworkspace version
            getattr(space,'import')(space1st.var('mu_{0}'.format(mcLabel)))
            getattr(space,'import')(space1st.var('sigma_MC_{0}1'.format(mcLabel)))
            getattr(space,'import')(space1st.var('sigma_MC_{0}2'.format(mcLabel)))
            getattr(space,'import')(space1st.var('sigma_MC_{0}3'.format(mcLabel)))
            getattr(space,'import')(space1st.var('frac_{0}1'.format(mcLabel)))
            getattr(space,'import')(space1st.var('frac_{0}2'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('bsMultiplier'))
            numTag='numBs'
            mcNum   =space2nd.var(numTag)
            space.var('mu_{0}'.format(mcLabel))       .setConstant(True)
            space.var('sigma_MC_{0}1'.format(mcLabel)).setConstant(True)
            space.var('sigma_MC_{0}2'.format(mcLabel)).setConstant(True)
            space.var('sigma_MC_{0}3'.format(mcLabel)).setConstant(True)
            space.var('frac_{0}1'.format(mcLabel))    .setConstant(True)
            space.var('frac_{0}2'.format(mcLabel))    .setConstant(True)

            space.var('bsMultiplier').setConstant(False)
            space.factory('Product::sig_{label}1({{ bsMultiplier,{sigma} }})'.format(label=fitLabel,sigma='sigma_MC_{0}1'.format(mcLabel)))
            space.factory('Product::sig_{label}2({{ bsMultiplier,{sigma} }})'.format(label=fitLabel,sigma='sigma_MC_{0}2'.format(mcLabel)))
            space.factory('Product::sig_{label}3({{ bsMultiplier,{sigma} }})'.format(label=fitLabel,sigma='sigma_MC_{0}3'.format(mcLabel)))

            space.factory('Gaussian::gPDF_{label}1({x},{mean},{sigma})'.format(label=fitLabel,x=varName,mean='mu_{0}'.format(mcLabel),sigma='sig_{0}1'.format(fitLabel)))
            space.factory('Gaussian::gPDF_{label}2({x},{mean},{sigma})'.format(label=fitLabel,x=varName,mean='mu_{0}'.format(mcLabel),sigma='sig_{0}2'.format(fitLabel)))
            space.factory('Gaussian::gPDF_{label}3({x},{mean},{sigma})'.format(label=fitLabel,x=varName,mean='mu_{0}'.format(mcLabel),sigma='sig_{0}3'.format(fitLabel)))

            space.factory('SUM::gPDF_{label}({frac1}*{pdf1},{frac2}*{pdf2},{pdf3})'.format(
                label=fitLabel,
                frac1='frac_{0}1'.format(mcLabel),pdf1='gPDF_{0}1'.format(fitLabel),
                frac2='frac_{0}2'.format(mcLabel),pdf2='gPDF_{0}2'.format(fitLabel),
                pdf3='gPDF_{0}3'.format(fitLabel),
                ))
            space.factory('ExtendPdf::eSigModel_{label}(gPDF_{label},{num})'.format(label=fitLabel,num=numTag))

            ePDFsList.append({'tag':'Bs','name':'eSigModel_{llabel}'.format(llabel=fitLabel)})
            print '--- Block ending to build Sig Model in section [{0}] ---'.format(label)
        else:
            print '--- Block start  to build Sig Model in section [{0}] sideband only!---'.format(label)
            mass=space.var(varName).setRange('Lside',5.1,5.2)
            mass=space.var(varName).setRange('Rside',5.35,5.5)
            fitRange=[]
            fitRange.append('Lside')
            fitRange.append('Rside')
            print '--- Block ending to build Sig Model in section [{0}] sideband only!---'.format(label)



        if buildBKGModel:
            print '--- Block start to build Bkg Model in section [{0}] ---'.format(label)
            # build rooworkspace version
            # # build particles background
            # nameBkgs=[{'tag':'bD','name':'kPDF_bdDist_antiBdK892MC'},{'tag':'Bs','name':'kPDF_bdDist_BsFMC'}]
            # numBkgNames=['fracbDNum_inBdDist','fracBsNum_inBdDist']

            # for idx,bkg in enumerate(nameBkgs):
            #     print 'idx = {0}, name = {1}'.format(idx,bkg['name'])
            #     getattr(space,'import')(space2nd.pdf(bkg['name']))
            #     space.factory('ExtendPdf::eBkgModel_{label}({pdf},{num})'.format(label=bkg['name'],pdf=bkg['name'],num=numBkgNames[idx]))
            #     ePDFsList.append({'tag':bkg['tag'],'name':'eBkgModel_{llabel}'.format(llabel=bkg['name'])})
            # bulid combinatorial background
            nameComb='pPDF_{0}'.format(fitLabel)
            numCombName='numCombBkg_{0}'.format(fitLabel)
            space.factory('p1_{label}[0.01,-5.,5.]'.format(label=fitLabel))

            space.factory('{name}[{initVal},{minVal},{maxVal}]'.format(name=numCombName,
                initVal=2000.,minVal=0.,maxVal=totNum))
            space.factory('Polynomial::{name}({x},{{ {c1} }})'.format(name=nameComb,x=varName,c1='p1_{0}'.format(fitLabel)))
            space.factory('ExtendPdf::e{name}({pdf},{num})'.format(name=nameComb,pdf=nameComb,num=numCombName))
            ePDFsList.append({'tag':'comb','name':'e'+nameComb})
            print '--- Block ending to build Bkg Model in section [{0}] ---'.format(label)




        # build total model and fit
        if buildBKGModel and performTotalFit:
            print '--- Block start to build Tot Model in section [{0}] ---'.format(label)
            ePdfSet=RooArgList()
            for ePDF in ePDFsList:
                print ePDF
                print space.pdf(ePDF['name']).GetName()
                ePdfSet.add(space.pdf(ePDF['name']))

            totPdf=RooAddPdf('totPdf_{0}'.format(label),'totPdf_{0}'.format(label),ePdfSet)
            if not buildSigModel:
                fitRange=','.join(fitRange)
            #fitRes=totPdf.fitTo(dataset.reduce('{x}>5.25&&{x}<5.5'.format(x=varName)),RooFit.Save(True),RooFit.Range(fitRange))
            #fitRes=totPdf.fitTo(dataset,RooFit.Save(True),RooFit.Range(fitRange))


            #xframe=space.var(varName).frame(RooFit.Title("load {0} Fit for check".format(varName)),RooFit.Range(fitRange))
            #dataset.plotOn(xframe,RooFit.Name('data'))
            #totPdf.plotOn(xframe, RooFit.Name('totModel'),RooFit.LineColor(2))
            #for pdf in ePDFsList:
            #    setup=ColorSetup[pdf['tag']]
            #    totPdf.plotOn(xframe,RooFit.Name(pdf['tag']),RooFit.Components(pdf['name']),
            #            RooFit.LineColor(setup['color']),RooFit.LineStyle(setup['style']),RooFit.LineWidth(4))

            #xframe.Draw()
            #fitres=fitRes
            #SaveResult(
            #        origPlot=xframe,
            #        origVar=space.var(varName),
            #        data={'content':dataset},
            #        totPDF={'content':totPdf},
            #        label=label,
            #        fitDir=fitDir,
            #        figDir=figDir,
            #        )
            print '--- Block ending to build Tot Model in section [{0}] ---'.format(label)
    # build Bs model end }}}
    recTime('build Bs interval')

    # data driven checking {{{
    if checkRawBsData:
        pureBdSelection='bdMass>5.15&&bdMass<5.4&&kpiMass>0.85&&kpiMass<0.95'
        purebDSelection='bdbarMass>5.15&&bdbarMass<5.4&&kpibarMass>0.85&&kpibarMass<0.95'
        pureBsSelection='bsMass>5.3&&bsMass<5.5&&kkMass<1.03&&kkMass>1.01'
        pureData=loadDatasetBs.reduce(pureBsSelection)
        mass=massBs
        fitRange='dataDrivenBs'
        sigPdf='eSigModel_BsBKG'
        bkgPdf='epPDF_BsBKG'
        print 'bkg pdf : {0}'.format(space.pdf(bkgPdf).GetName())
        mass.setRange(fitRange,5.3,5.5)


        #c1Var=RooRealVar('c1','c1',-0.5,-5.,5.)
        #bkgPdf=RooPolynomial('bkgpdf','bkgpdf',mass,RooArgList(c1Var))
        #numbkg=RooRealVar('numbkg','numbkg',200,0.,5000.)
        #ebkg=RooExtendPdf('ebkg','ebkg',bkgPdf,numbkg)
        #tPdf=RooAddPdf('tot','tot',RooArgList(esig,ebkg))
        argset=RooArgList(space.pdf(sigPdf),space.pdf(bkgPdf))
        tPdf=RooAddPdf('tot','tot',argset)
        #space.factory('SUM::totPdf_{name}({{{sig},{bkg}}})'.format(name=fitRange,sig=sigPdf,bkg=bkgPdf))
        #tPdf=space.pdf('totPdf_{name}'.format(name=fitRange))

        fitRes=tPdf.fitTo(pureData,RooFit.Save(True),RooFit.Range(fitRange))

        xframe=mass.frame(RooFit.Range(fitRange),RooFit.Title(fitRange))
        pureData.plotOn(xframe,RooFit.Name('data'))
        tPdf.plotOn(xframe,RooFit.Name('totPdf'))
        tPdf.plotOn(xframe,RooFit.Name('sig'),RooFit.Components(sigPdf),RooFit.LineColor( 2))
        #space.pdf(bkgPdf).plotOn(xframe)
        tPdf.plotOn(xframe,RooFit.Name('bkg'),RooFit.Components(bkgPdf),RooFit.LineColor(30))
        xframe.Draw()
        canv.SaveAs(tMPfIG)
        fitres=fitRes
        SaveResult(
                origPlot=xframe,
                origVar=mass,
                data={'content':pureData},
                totPDF={'content':tPdf},
                fitres=fitres,
                label=fitRange,
                fitDir=fitDir,
                figDir=figDir,
                )
        space.var('numBs').setConstant(True)

    # data driven checking end }}}

    recTime('data driven checking interval')
    # build simultaneous bd model {{{
    if directsimBdFitData:
        label='BdSimul'
        varList=['bdMass','bdbarMass']
        print '--- Block start to build simultaneous model and fitting in section [{0}] ---'.format(label)
        # construct catetory
        cat=RooCategory(label,label)
        for simulComp in simulComponents:
            cat.defineType(simulComp['cat'])
            print 'catetory :: {0}'.format(simulComp['cat'])

        # build simultaneous pdf with only 1 category.
        simulPdf=RooSimultaneous('simPdf','simPdf',cat)
        for simulComp in simulComponents:
            simulPdf.addPdf(simulComp['pdf'],simulComp['cat'])

        # build "complex" dataset
        combData=RooDataSet('combData','combData', RooArgSet(massBd,massbD),RooFit.Index(cat),
                RooFit.Import(simulComponents[0]['cat'],loadDatasetBd),
                RooFit.Import(simulComponents[1]['cat'],loadDatasetbD),
                )

        fitRes=simulPdf.fitTo(combData,RooFit.Save(True),RooFit.Minos(useMinos))

        # plot on category
        frames=[]
        xvars=[]
        for idx,xName in enumerate(varList):
            xvar=space.var(xName)
            simulComp=simulComponents[idx]
            frame1=xvar.frame(RooFit.Title('simultaneous fit'),RooFit.Name(xName))
            combData.plotOn(frame1,RooFit.Name('data'),RooFit.Cut('{catObj}=={catObj}::{catIdx}'.format(catObj=label,catIdx=simulComp['cat'])))
            simulPdf.plotOn(frame1,RooFit.Name('totModel'),RooFit.Slice(cat,'{catIdx}'.format(catIdx=simulComp['cat'])),RooFit.ProjWData(RooArgSet(cat),combData),RooFit.LineColor(2))
            for pdf in simulComp['components']:
                setup=ColorSetup[pdf['tag']]
                simulPdf.plotOn(frame1,RooFit.Name(pdf['tag']),RooFit.Slice(cat,'{catIdx}'.format(catIdx=simulComp['cat'])),RooFit.ProjWData(RooArgSet(cat),combData),
                        RooFit.Components(pdf['name']),RooFit.LineColor(setup['color']),RooFit.LineStyle(setup['style']),RooFit.LineWidth(4))

            xvars.append(xvar)
            frames.append(frame1)
        fitres=fitRes
        SaveSimulResult(
                origPlot=frames,
                origVar=xvars,
                data=[
                    {'content':combData.reduce('{catObj}=={catObj}::{catIdx}'.format(catObj=label,catIdx=simulComponents[0]['cat']))},
                    {'content':combData.reduce('{catObj}=={catObj}::{catIdx}'.format(catObj=label,catIdx=simulComponents[1]['cat']))},
                    ],
                totPDF=[
                    {'content':simulComponents[0]['pdf']},
                    {'content':simulComponents[1]['pdf']},
                    ],
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                )

        print '--- Block ending to build simultaneous model and fitting in section [{0}] ---'.format(label)
        print 'tot data entries {0}'.format(loadDatasetBd.sumEntries())

        print '--- Block Ending to build {0} ---'.format(label)
    # build simultaneous bd model end }}}
    recTime('bd simultaneous interval')

    #space.var('numBd').setConstant(True)
    #space.var('numbD').setConstant(True)

    # build Lb Model {{{
    fitres=None
    if LbModelBuilding:
        label='LbModel'
        print '--- Block start to build {0} ---'.format(label)

        buildSigModel=True
        buildBKGModel=True
        performTotalFit=True
        mcLabel='lbtkDist_lbtkMC'
        fitLabel='ShortRangeLbFit'
        varName='lbtkMass'
        ePDFsList=[]
        fitRange='sigRangeLb'

        dataset=loadDatasetLb.reduce(ptCut)

        if buildSigModel:
            print '--- Block start to build Sig Model in section [{0}] ---'.format(label)
            numTag='numLb'

            # rooworkspace version
            getattr(space,'import')(space1st.var('mu_{0}'.format(mcLabel)))
            getattr(space,'import')(space1st.var('sigma_MC_{0}1'.format(mcLabel)))
            getattr(space,'import')(space1st.var('sigma_MC_{0}2'.format(mcLabel)))
            getattr(space,'import')(space1st.var('frac_{0}1'.format(mcLabel)))
            getattr(space,'import')(space2nd.var('bsMultiplier'))
            space.var('mu_{0}'.format(mcLabel)).setConstant(True)
            space.var('sigma_MC_{0}1'.format(mcLabel)).setConstant(True)
            space.var('sigma_MC_{0}2'.format(mcLabel)).setConstant(True)
            space.var('frac_{0}1'.format(mcLabel)).setConstant(True)
            mcNum=space.var(numTag)

            # apply data-MC difference to width of gaussians.
            space.factory('Product::sig_{label}1({{ bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma='sigma_MC_{0}1'.format(mcLabel)))
            space.factory('Product::sig_{label}2({{ bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma='sigma_MC_{0}2'.format(mcLabel)))
            space.factory('Gaussian::gPartPDF_{label}1({massVar},mu_{label},sig_{label}1)'.format(massVar=varName,label=mcLabel))
            space.factory('Gaussian::gPartPDF_{label}2({massVar},mu_{label},sig_{label}2)'.format(massVar=varName,label=mcLabel))
            space.factory('SUM::gPDF_{llabel}(frac_{label}1*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,llabel=fitLabel))
            space.factory('ExtendPdf::eSigModel_{llabel}(gPDF_{llabel},{num})'.format(llabel=fitLabel,num=numTag))


            # build extended PDF
            ePDFsList.append({'tag':'Lb','name':'eSigModel_{llabel}'.format(llabel=fitLabel)})
            print '--- Block ending to build Sig Model in section [{0}] ---'.format(label)
        else:
            print '--- Block start  to build Sig Model in section [{0}] sideband only!---'.format(label)
            var=space.var(varName)
            var.setRange('Lside',var.getMin(),5.58)
            var.setRange('Rside',5.66,var.getMax())
            fitRange=[]
            fitRange.append('Lside')
            fitRange.append('Rside')
            print '--- Block ending to build Sig Model in section [{0}] sideband only!---'.format(label)



        if buildBKGModel:
            print '--- Block start to build Bkg Model in section [{0}] ---'.format(label)
            # bulid combinatorial background
            # build number variable to comb bkg
            numCombName='numCombBkg_{0}'.format(fitLabel)
            space.factory('{name}[{initVal},{minVal},{maxVal}]'.format(name=numCombName,
                initVal=dataset.sumEntries(),minVal=0.,maxVal=dataset.sumEntries()*2.0))

            # build polynomial comb bkg
            nameComb='pPDF_{0}'.format(fitLabel)
            # space.factory('cp1[-0.01,-3.,50.]')

            space.factory('cp1[0.3,-2.,2.]')
            space.factory('cp2[-0.7,-3.,7.]')

            #space.factory('cp1[0.3,-2.,2.]')
            #space.factory('cp2[-0.7,-2.,2.]')
            #space.factory('cp3[-0.07,-4.,4.]')

            space.factory('x0[-5.498]')
            space.factory('Addition::X({{ {x},x0 }})'.format(x=varName))
            space.factory('Polynomial::{name}(X,{{cp1,cp2}})'.format(name=nameComb))
            #space.factory('Polynomial::{name}(X,{{cp1,cp2,cp3}})'.format(name=nameComb))

            # build extend pdf
            space.factory('ExtendPdf::e{name}({pdf},{num})'.format(name=nameComb,pdf=nameComb,num=numCombName))
            ePDFsList.append({'tag':'comb','name':'e'+nameComb})
            print '--- Block ending to build Bkg Model in section [{0}] ---'.format(label)




        # build total model and fit
        if buildBKGModel and performTotalFit:
            print '--- Block start to build Tot Model in section [{0}] ---'.format(label)
            ePdfSet=RooArgList()
            for ePDF in ePDFsList:
                print ePDF['name']
                ePdfSet.add(space.pdf(ePDF['name']))
                print ePDF['name'] +'   end'
            print 'test --- {0}'.format(['{0}, {1}'.format(ePDF['tag'],ePDF['name']) for ePDF in ePDFsList])

            totPdf=RooAddPdf('totPdf_{0}'.format(label),'totPdf_{0}'.format(label),ePdfSet)
            if not buildSigModel:
                fitRange=','.join(fitRange)
            var=space.var(varName)
            getattr(space,'import')(totPdf)

            # check x0 first, and set it as a constant
            data=dataset.reduce('{x}>{minVal}&&{x}<{maxVal}'.format(x=varName,minVal=var.getMin(),maxVal=var.getMax()))
            fitRes=totPdf.fitTo(data,RooFit.Save(True),RooFit.Range(fitRange),RooFit.Minos(useMinos),RooFit.NumCPU(4))


            xframe=space.var(varName).frame(RooFit.Title("load {0} Fit for check".format(varName)),RooFit.Range(fitRange))
            dataset.plotOn(xframe,RooFit.Name('data'))
            totPdf.plotOn(xframe, RooFit.Name('totModel'),RooFit.LineColor(2),RooFit.Normalization(data.sumEntries(),RooAbsReal.NumEvent))
            b=[]

            for pdf in ePDFsList:
                b.append(pdf['name'])
                setup=ColorSetup[pdf['tag']]
                totPdf.plotOn(xframe,RooFit.Name(pdf['tag']),RooFit.Components(pdf['name']),
                        RooFit.LineColor(setup['color']),RooFit.LineStyle(setup['style']),RooFit.LineWidth(4),
                        RooFit.Normalization(data.sumEntries(),RooAbsReal.NumEvent)
                        )


            xframe.Draw()
            fitres=fitRes
            SaveResult(
                    origPlot=xframe,
                    origVar=space.var(varName),
                    data={'content':dataset},
                    totPDF={'content':totPdf},
                    fitres=fitres,
                    label=label,
                    fitDir=fitDir,
                    figDir=figDir,
                    )
            params=totPdf.getParameters(RooArgSet(space.var(varName)))
            space.defineSet('parameters',params)
            space.defineSet('observable',RooArgSet(space.var(varName)))
            space.saveSnapshot('LbFitRes',params,True)
            CheckToyMC(space,totPdf,space.var(varName),'LbFitRes')
            print '--- Block ending to build Tot Model in section [{0}] ---'.format(label)
    # build Lb model end }}}
    recTime('build Lb model interval')
    # build lB Model {{{
    fitres=None
    if lBModelBuilding:
        label='lBModel'
        print '--- Block start to build {0} ---'.format(label)

        buildSigModel=True
        buildBKGModel=True
        performTotalFit=True
        mcLabel='lbtkbarDist_antilbtkMC'
        fitLabel='ShortRangelBFit'
        varName='lbtkbarMass'
        ePDFsList=[]
        fitRange='sigRangelB'

        dataset=loadDatasetlB.reduce(ptCut)

        if buildSigModel:
            print '--- Block start to build Sig Model in section [{0}] ---'.format(label)
            numTag='numlB'

            # rooworkspace version
            getattr(space,'import')(space1st.var('mu_{0}'.format(mcLabel)))
            getattr(space,'import')(space1st.var('sigma_MC_{0}1'.format(mcLabel)))
            getattr(space,'import')(space1st.var('sigma_MC_{0}2'.format(mcLabel)))
            getattr(space,'import')(space1st.var('frac_{0}1'.format(mcLabel)))
            #getattr(space,'import')(space2nd.var('bsMultiplier'))
            space.var('mu_{0}'.format(mcLabel)).setConstant(True)
            space.var('sigma_MC_{0}1'.format(mcLabel)).setConstant(True)
            space.var('sigma_MC_{0}2'.format(mcLabel)).setConstant(True)
            space.var('frac_{0}1'.format(mcLabel)).setConstant(True)
            mcNum=space.var(numTag)

            # apply data-MC difference to width of gaussians.
            space.factory('Product::sig_{label}1({{ bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma='sigma_MC_{0}1'.format(mcLabel)))
            space.factory('Product::sig_{label}2({{ bsMultiplier,{sigma} }})'.format(label=mcLabel,sigma='sigma_MC_{0}2'.format(mcLabel)))
            space.factory('Gaussian::gPartPDF_{label}1({massVar},mu_{label},sig_{label}1)'.format(massVar=varName,label=mcLabel))
            space.factory('Gaussian::gPartPDF_{label}2({massVar},mu_{label},sig_{label}2)'.format(massVar=varName,label=mcLabel))
            space.factory('SUM::gPDF_{llabel}(frac_{label}1*gPartPDF_{label}1,gPartPDF_{label}2)'.format(label=mcLabel,llabel=fitLabel))
            space.factory('ExtendPdf::eSigModel_{llabel}(gPDF_{llabel},{num})'.format(llabel=fitLabel,num=numTag))


            # build extended PDF
            ePDFsList.append({'tag':'lB','name':'eSigModel_{llabel}'.format(llabel=fitLabel)})
            print '--- Block ending to build Sig Model in section [{0}] ---'.format(label)
        else:
            print '--- Block start  to build Sig Model in section [{0}] sideband only!---'.format(label)
            var=space.var(varName)
            var.setRange('Lside',var.getMin(),5.58)
            var.setRange('Rside',5.66,var.getMax())
            fitRange=[]
            fitRange.append('Lside')
            fitRange.append('Rside')
            print '--- Block ending to build Sig Model in section [{0}] sideband only!---'.format(label)



        if buildBKGModel:
            print '--- Block start to build Bkg Model in section [{0}] ---'.format(label)
            # bulid combinatorial background
            # build number variable to comb bkg
            numCombName='numCombBkg_{0}'.format(fitLabel)
            space.factory('{name}[{initVal},{minVal},{maxVal}]'.format(name=numCombName,
                initVal=dataset.sumEntries(),minVal=0.,maxVal=dataset.sumEntries()*2.0))

            # build polynomial comb bkg
            nameComb='pPDF_{0}'.format(fitLabel)
            # space.factory('cp1[-0.01,-3.,50.]')

            space.factory('cp1_[0.3,-2.,2.]')
            space.factory('cp2_[-0.7,-3.,7.]')

            #space.factory('cp1_[0.3,-2.,2.]')
            #space.factory('cp2_[-0.7,-2.,2.]')
            #space.factory('cp3_[-0.07,-4.,4.]')

            space.factory('x0_[-5.498]')
            space.factory('Addition::X_({{ {x},x0_ }})'.format(x=varName))
            space.factory('Polynomial::{name}(X_,{{cp1_,cp2_}})'.format(name=nameComb))
            #space.factory('Polynomial::{name}(X_,{{cp1_,cp2_,cp3_}})'.format(name=nameComb))

            # build extend pdf
            space.factory('ExtendPdf::e{name}({pdf},{num})'.format(name=nameComb,pdf=nameComb,num=numCombName))
            ePDFsList.append({'tag':'comb','name':'e'+nameComb})
            print '--- Block ending to build Bkg Model in section [{0}] ---'.format(label)




        # build total model and fit
        if buildBKGModel and performTotalFit:
            print '--- Block start to build Tot Model in section [{0}] ---'.format(label)
            ePdfSet=RooArgList()
            for ePDF in ePDFsList:
                print ePDF['name']
                ePdfSet.add(space.pdf(ePDF['name']))
                print ePDF['name'] +'   end'
            print 'test --- {0}'.format(['{0}, {1}'.format(ePDF['tag'],ePDF['name']) for ePDF in ePDFsList])

            totPdf=RooAddPdf('totPdf_{0}'.format(label),'totPdf_{0}'.format(label),ePdfSet)
            if not buildSigModel:
                fitRange=','.join(fitRange)
            var=space.var(varName)
            getattr(space,'import')(totPdf)

            # check x0 first, and set it as a constant
            data=dataset.reduce('{x}>{minVal}&&{x}<{maxVal}'.format(x=varName,minVal=var.getMin(),maxVal=var.getMax()))
            #totPdf.fitTo(data,RooFit.Range(fitRange),RooFit.Minos(False),RooFit.NumCPU(4))
            #space.var('x0').setConstant(True)
            fitRes=totPdf.fitTo(data,RooFit.Save(True),RooFit.Range(fitRange),RooFit.Minos(useMinos),RooFit.NumCPU(4))


            xframe=space.var(varName).frame(RooFit.Title("load {0} Fit for check".format(varName)),RooFit.Range(fitRange))
            dataset.plotOn(xframe,RooFit.Name('data'))
            totPdf.plotOn(xframe, RooFit.Name('totModel'),RooFit.LineColor(2),RooFit.Normalization(data.sumEntries(),RooAbsReal.NumEvent))
            b=[]

            for pdf in ePDFsList:
                b.append(pdf['name'])
                setup=ColorSetup[pdf['tag']]
                totPdf.plotOn(xframe,RooFit.Name(pdf['tag']),RooFit.Components(pdf['name']),
                        RooFit.LineColor(setup['color']),RooFit.LineStyle(setup['style']),RooFit.LineWidth(4),
                        RooFit.Normalization(data.sumEntries(),RooAbsReal.NumEvent)
                        )


            xframe.Draw()
            fitres=fitRes
            SaveResult(
                    origPlot=xframe,
                    origVar=space.var(varName),
                    data={'content':dataset},
                    totPDF={'content':totPdf},
                    fitres=fitres,
                    label=label,
                    fitDir=fitDir,
                    figDir=figDir,
                    )
            params=totPdf.getParameters(RooArgSet(space.var(varName)))
            space.defineSet('parameters',params)
            space.defineSet('observable',RooArgSet(space.var(varName)))
            space.saveSnapshot('lBFitRes',params,True)
            CheckToyMC(space,totPdf,space.var(varName),'lBFitRes')
            print '--- Block ending to build Tot Model in section [{0}] ---'.format(label)
    # build lB model end }}}
    recTime('build lB model interval')




    canv.Clear()



canv.SaveAs(tMPfIG+']')
outFile.cd()
space.Write()
outFile.Close()
#print 'Bd dataset entries() = {0}, in signal region {1}'.format(loadDatasetBd.sumEntries(),loadDatasetBd.reduce('bdMass>5.1&&bdMass<5.5').sumEntries())
os.system('mv {0} {1}'.format(tMPrOOTnAME,storeFileName))
os.system('mv {0} {1}'.format(tMPfIG,storeFigName))
#print 'bD dataset entries() = {0}, in signal region {1}'.format(loadDatasetbD.sumEntries(),loadDatasetbD.reduce('bdbarMass>5.1&&bdbarMass<5.5').sumEntries())

txtRecFile.close()
