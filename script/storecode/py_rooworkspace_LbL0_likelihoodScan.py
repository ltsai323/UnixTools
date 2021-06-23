#!/usr/bin/env python
# check fitting result in different Lambda0 mass cut.

import os
from array import array
from ROOT import TLegend, TBox, TLine
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis, TPad, TLine, TGraphErrors, TRatioPlot, TGraph, gRandom, TNtupleD
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsData, RooPlot, RooAbsReal, RooExtendPdf, RooMinuit
import time


nBinsCheck=10
#dataFileName='result_flatNtuple_NoSelection.root'
#dataFileName='result_flatNtuple_LbTk_preSelection_noKinematicCut.root'
#storeFileName='store_root/workspace_extraStep_2nd_stabilityLbCheck_noKineCut.root'
#storeFigName='store_fig/pdf_workspace_extraStep_2nd_stabilityLbCheck_noKineCut.pdf'

dataFileName='result_flatNtuple_LbL0_preSelection_noKinematicCut.root'
storeFileName='store_root/workspace_LbL0_stabilityLbCheck_withoutKineCut.root'
storeFigName='store_fig/pdf_workspace_LbL0_stabilityLbCheck_withoutKineCut.pdf'

tMPrOOTnAME='tmp.root'
tMPfIG='tmp.pdf'
txtRecFile=open('log_timeRec.txt','w')
currenttime=time.time()
rectime=currenttime
txtRecFile.write('start run job')


outFile=TFile(tMPrOOTnAME,'recreate')
figDir=outFile.mkdir('figs')
fitDir=outFile.mkdir('fitRes')
ColorSetup={
        'Lb':{'color': 8,'style':2},
        'lB':{'color':30,'style':2},
        'comb':{'color':13,'style':5},
        }


# set output message level
RooMsgService.instance().setGlobalKillBelow(4)

useMinos=True

def NewCanvas(name='c1'):
    canv=TCanvas(name,'',1000,1000)
    canv.SetFillColor(4000)
    canv.SetFillStyle(4000)
    return canv
canv=NewCanvas()
canv.SaveAs(tMPfIG+'[')
TGaxis.SetMaxDigits(3)


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
def SimpleSaveToFile(**kwargs):
    kwargs['dir'].cd()
    kwargs['object'].Write(kwargs['label'])
    return None
def CheckToyMC(space,pdf,var,snapshot):
    toyData=pdf.generate(RooArgSet(var),10000)
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

def recTime(mesg):
    global currenttime
    rectime=currenttime
    currenttime=time.time()
    txtRecFile.write('{0} in {1} minutes\n'.format(mesg,int((currenttime-rectime)/60)))
# def functions end }}}

recTime('def funcs')
space=RooWorkspace('space',False)

# new parameters
space.factory('lbl0Mass[5.4,5.9]')
space.factory('tktkMass[0.5,2.0]')


########## load workspace ####################
workspaceFile1=TFile.Open('store_root/workspace_0thStep_LbL0Shape.root')
space1st=workspaceFile1.Get('space')
space1st.SetName('space1st')


load2016Data=True
if load2016Data:
    toyCheck=False

    scanLikelihoodLb=True
    scanLikelihoodlB=True
    LbStabilityFit=False

    inFile16=TFile.Open(dataFileName)
    inN16=inFile16.Get('pLbL0/2016Data')
    inn16=inFile16.Get('nLbL0/2016Data')

    # load parameters from other workspace and import them in current workspace
    massLb=space.var('lbl0Mass')
    massTkTk=space.var('tktkMass')


    massLb.setBins(50)

    massLb.setRange('sigRangeLb',5.4,5.9)

    loadDatasetLb=RooDataSet('loadDatasetLb','loadData16',inN16,RooArgSet(massLb,massTkTk)).reduce('tktkMass>1.105&&tktkMass<1.130')
    loadDatasetlB=RooDataSet('loadDatasetlB','loadData16',inn16,RooArgSet(massLb,massTkTk)).reduce('tktkMass>1.105&&tktkMass<1.130')
    totNum=loadDatasetLb.sumEntries()
    space.factory('numLb[{0},-1000.,{1}]'.format(space1st.var('numLb').getVal(),totNum))

    simulComponents=[]

    # scan Lb likelihood {{{
    # jack's profile likelihood scan
    if scanLikelihoodLb:
        label='LbL0ScanLikelihood'

        varName='lbl0Mass'
        figDir.cd()

        var=space.var(varName)
        model=space1st.pdf('totPdf_Run2016Data_pLbL0')
        #dataset=model.generate(RooArgSet(space.var('lbtkMass')),10000)
        dataset=loadDatasetLb.reduce('{x}>{minVal}&&{x}<{maxVal}'.format(x=varName,minVal=var.getMin(),maxVal=var.getMax()))
        nll=model.createNLL(dataset)
        fitres=model.fitTo(dataset,RooFit.Save(True),RooFit.Minos(useMinos))


        plot=var.frame(RooFit.Title('data fit {0}'.format(label)))
        dataset.plotOn(plot)
        model.plotOn(plot,RooFit.Normalization( dataset.sumEntries(),RooAbsReal.NumEvent))
        SaveResult(
                origPlot=plot,
                origVar=var,
                data={'content':dataset},
                totPDF={'content':model},
                fitres=fitres,
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                absNumNormalize=dataset.sumEntries()
                )


        scanVarList=[
                {'var':'c1_Run2016Data_pLbL0'        ,'range':[-2.,0.2]     ,'title':'1st var of polynomial','tag':''},
                {'var':'c2_Run2016Data_pLbL0'        ,'range':[-3.,1.0]     ,'title':'2nd var of polynomial','tag':''},

                #{'var':'cp1'        ,'range':[-2.,2.]     ,'title':'1st var of polynomial','tag':''},
                #{'var':'cp2'        ,'range':[-2.,2.]     ,'title':'2nd var of polynomial','tag':''},
                #{'var':'cp3'        ,'range':[-4,4.]     ,'title':'3rd var of polynomial','tag':''},
                ]
        for varInfo in scanVarList:
            nll_scan=TH1D('nll_scan_{0}{1}'.format(varInfo['var'],varInfo['tag']),'likelihood scan in '+varInfo['title'],
                    nBinsCheck,varInfo['range'][0],varInfo['range'][1])
            nll_profscan=TH1D('nll_profscan_{0}{1}'.format(varInfo['var'],varInfo['tag']),'profile likelihood scan in '+varInfo['title'],
                    nBinsCheck,varInfo['range'][0],varInfo['range'][1])
            var=space1st.var(varInfo['var'])

            # likehood scan
            for nBin in range(nll_scan.GetNbinsX()):
                binIdx=nBin+1
                var.setVal(nll_scan.GetBinCenter(binIdx))
                nll_scan.SetBinContent(binIdx,(nll.getVal()-fitres.minNll())*2.)

            # profile likehood scan
            for nBin in range(nll_profscan.GetNbinsX()):
                binIdx=nBin+1
                var.setVal(nll_profscan.GetBinCenter(binIdx))
                var.setConstant(True)
                model.fitTo(dataset)
                nll_profscan.SetBinContent(binIdx,(nll.getVal()-fitres.minNll())*2.)

                mesg='nll: {0}, minNLL= {1}'.format(nll.getVal(),fitres.minNll())
                recTime(mesg)
                var.setConstant(False)

            nll_scan.SetStats(False)
            nll_scan.SetLineWidth(2)
            nll_scan.GetXaxis().SetTitle(varInfo['var'])
            nll_profscan.Draw('axis')
            canv.Update()

            box=TBox()
            box.SetFillColor(7)
            bestVal=fitres.floatParsFinal().find(varInfo['var'])
            box.DrawBox(
                    bestVal.getVal()+bestVal.getErrorLo(),canv.GetUymin(),
                    bestVal.getVal()+bestVal.getErrorHi(),canv.GetUymax()
                    )
            nll_scan.Draw('csame')

            nll_profscan.SetLineWidth(2)
            nll_profscan.SetLineColor(2)
            nll_profscan.Draw('csame')
            outFile.cd()
            nll_scan.Write()
            nll_profscan.Write()

            canv.SaveAs(tMPfIG)

            SimpleSaveToFile(
                    dir=figDir,
                    object=nll_profscan,
                    label=nll_profscan.GetName()
                    )
            SimpleSaveToFile(
                    dir=figDir,
                    object=nll_scan,
                    label=nll_scan.GetName()
                    )



    # scan Lb likelihood end }}}

    # scan lB likelihood {{{
    # jack's profile likelihood scan
    if scanLikelihoodlB:
        label='LbLoScanLikelihood'

        varName='lbl0Mass'
        figDir.cd()

        var=space.var(varName)
        model=space1st.pdf('totPdf_Run2016Data_nLbL0')
        #dataset=model.generate(RooArgSet(space.var('lbtkMass')),10000)
        dataset=loadDatasetlB.reduce('{x}>{minVal}&&{x}<{maxVal}'.format(x=varName,minVal=var.getMin(),maxVal=var.getMax()))
        nll=model.createNLL(dataset)
        fitres=model.fitTo(dataset,RooFit.Save(True),RooFit.Minos(useMinos))


        plot=var.frame(RooFit.Title('data fit {0}'.format(label)))
        dataset.plotOn(plot)
        model.plotOn(plot,RooFit.Normalization( dataset.sumEntries(),RooAbsReal.NumEvent))
        SaveResult(
                origPlot=plot,
                origVar=var,
                data={'content':dataset},
                totPDF={'content':model},
                fitres=fitres,
                label=label,
                fitDir=fitDir,
                figDir=figDir,
                absNumNormalize=dataset.sumEntries()
                )


        scanVarList=[
                {'var':'c1_Run2016Data_nLbL0'        ,'range':[-1.5,0.2]     ,'title':'1st var of polynomial','tag':''},
                {'var':'c2_Run2016Data_nLbL0'        ,'range':[-3.,0.2]     ,'title':'2nd var of polynomial','tag':''},

                #{'var':'cp1'        ,'range':[-2.,2.]     ,'title':'1st var of polynomial','tag':''},
                #{'var':'cp2'        ,'range':[-2.,2.]     ,'title':'2nd var of polynomial','tag':''},
                #{'var':'cp3'        ,'range':[-4,4.]     ,'title':'3rd var of polynomial','tag':''},
                ]
        for varInfo in scanVarList:
            nll_scan=TH1D('nll_scan_{0}{1}'.format(varInfo['var'],varInfo['tag']),'likelihood scan in '+varInfo['title'],
                    nBinsCheck,varInfo['range'][0],varInfo['range'][1])
            nll_profscan=TH1D('nll_profscan_{0}{1}'.format(varInfo['var'],varInfo['tag']),'profile likelihood scan in '+varInfo['title'],
                    nBinsCheck,varInfo['range'][0],varInfo['range'][1])
            var=space1st.var(varInfo['var'])

            # likehood scan
            for nBin in range(nll_scan.GetNbinsX()):
                binIdx=nBin+1
                var.setVal(nll_scan.GetBinCenter(binIdx))
                nll_scan.SetBinContent(binIdx,(nll.getVal()-fitres.minNll())*2.)

            # profile likehood scan
            for nBin in range(nll_profscan.GetNbinsX()):
                binIdx=nBin+1
                var.setVal(nll_profscan.GetBinCenter(binIdx))
                var.setConstant(True)
                model.fitTo(dataset)
                nll_profscan.SetBinContent(binIdx,(nll.getVal()-fitres.minNll())*2.)

                mesg='nll: {0}, minNLL= {1}'.format(nll.getVal(),fitres.minNll())
                recTime(mesg)
                var.setConstant(False)

            nll_scan.SetStats(False)
            nll_scan.SetLineWidth(2)
            nll_scan.GetXaxis().SetTitle(varInfo['var'])
            nll_profscan.Draw('axis')
            canv.Update()

            box=TBox()
            box.SetFillColor(7)
            bestVal=fitres.floatParsFinal().find(varInfo['var'])
            box.DrawBox(
                    bestVal.getVal()+bestVal.getErrorLo(),canv.GetUymin(),
                    bestVal.getVal()+bestVal.getErrorHi(),canv.GetUymax()
                    )
            nll_scan.Draw('csame')

            nll_profscan.SetLineWidth(2)
            nll_profscan.SetLineColor(2)
            nll_profscan.Draw('csame')
            outFile.cd()
            nll_scan.Write()
            nll_profscan.Write()

            canv.SaveAs(tMPfIG)

            SimpleSaveToFile(
                    dir=figDir,
                    object=nll_profscan,
                    label=nll_profscan.GetName()
                    )
            SimpleSaveToFile(
                    dir=figDir,
                    object=nll_scan,
                    label=nll_scan.GetName()
                    )



    # scan lB likelihood end }}}


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
