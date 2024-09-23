#!/usr/bin/env python
# check fitting result in different Lambda0 mass cut.

import os
from array import array
from ROOT import TLegend, TBox, TLine
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis, TPad, TLine, TGraphErrors, TGraph, gRandom, TNtupleD
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsData, RooPlot, RooAbsReal, RooExtendPdf, RooMinuit
import time









dataFileName='result_flatNtuple_LbL0_preSelection_noKinematicCut.root'
storeFileName='store_root/keepMCevent_3rdStep_LbL0Shape_sysmaticErrFit_noKinematicCut_{0}.root'.format(ptRange)
storeFigName='store_fig/pdf_keepMCevent_3rdStep_LbL0Shape_sysmaticErrFit_noKinematicCut_{0}.pdf'.format(ptRange)
storeTXTName='log_keepMCevent_3rdStep_LbL0Shape_sysmaticErrFit_noKinematicCut_{0}.txt'.format(ptRange)
storeTXT=open(storeTXTName,'w')

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
space.factory('lbl0Pt[0.,200.]')


########## load workspace ####################
workspaceFile1=TFile.Open('store_root/keepMCevent_0thStep_LbL0Shape_noKinematicCut.{0}.root'.format(ptRange))
space1st=workspaceFile1.Get('space')
space1st.SetName('space1st')
spaceExt=space1st


load2016Data=True
if load2016Data:
    toyCheck=False

    sysFitLb=True
    sysFitlB=True
    LbStabilityFit=False

    inFile16=TFile.Open(dataFileName)
    inN16=inFile16.Get('pLbL0/2016Data')
    inn16=inFile16.Get('nLbL0/2016Data')

    # load parameters from other workspace and import them in current workspace
    massLb=space.var('lbl0Mass')
    massTkTk=space.var('tktkMass')


    massLb.setBins(50)

    massLb.setRange('sigRangeLb',5.4,5.9)

    loadDatasetLb=RooDataSet('loadDatasetLb','loadData16',inN16,RooArgSet(massLb,massTkTk,space.var('lbl0Pt'))).reduce('tktkMass>1.110&&tktkMass<1.120 &&{0}'.format(ptCut))
    loadDatasetlB=RooDataSet('loadDatasetlB','loadData16',inn16,RooArgSet(massLb,massTkTk,space.var('lbl0Pt'))).reduce('tktkMass>1.110&&tktkMass<1.120 &&{0}'.format(ptCut))
    totNum=loadDatasetLb.sumEntries()
    space.factory('numLb[{0},-1000.,{1}]'.format(space1st.var('numLb').getVal(),totNum))

    simulComponents=[]

    # scan Lb likelihood {{{
    # jack's profile likelihood scan
    if sysFitLb:
        label='sysLbFit'

        numSig=spaceExt.var('numLb')
        numBkg=spaceExt.var('numCombBkg_Run2016Data_pLbL0')
        varName='lbl0Mass'
        figDir.cd()

        var=space.var(varName)
        model=space1st.pdf('totPdf_Run2016Data_pLbL0')
        #dataset=model.generate(RooArgSet(space.var('lbtkMass')),10000)
        dataset=loadDatasetLb.reduce('{x}>{minVal}&&{x}<{maxVal}'.format(x=varName,minVal=var.getMin(),maxVal=var.getMax()))
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

        snapNumSig=numSig.getVal()
        snapNumBkg=numBkg.getVal()


        totalVarList=[
                'c1_Run2016Data_pLbL0',
                'c2_Run2016Data_pLbL0',
                ]
        scanVarList=[
                {'var':'frac1_lbl0Dist_lbl0MC', 'title':'frac_sigGaus'},
                {'var':'mean_lbl0Dist_lbl0MC', 'title':'mean_sigGaus'},
                {'var':'sigma_MCfit_lbl0Dist_lbl0MC1', 'title':'width1_sigGaus'},
                {'var':'sigma_MCfit_lbl0Dist_lbl0MC2', 'title':'width2_sigGaus'},
                {'var':'data_MC_factor', 'title':'factor_dataMCFactor'},
                ]

        tmplist=[]
        # record how much variable needs to be scan.
        # values: 0.mean, 1.mean-err, 2.mean+err
        for varInfo in scanVarList:
            v=spaceExt.var(varInfo['var'])
            VAL=v.getVal()
            ERR=v.getError()
            fitList=[VAL,VAL-ERR,VAL+ERR]
            tmplist.append({'var':varInfo['var'],'values':fitList,'title':varInfo['title']})
        # record the variable not need to be scan.
        for varInfo in totalVarList:
            lostVar=True
            for rec in tmplist:
                if varInfo == rec['var']:
                    lostVar=False
            if lostVar:
                tmplist.append({'var':varInfo,'values':[spaceExt.var(varInfo).getVal()],
                                'title':'constraintTo'+varInfo})
        storeTXT.write('cat:              ' + ', '.join([v['var'] for v in tmplist]) + '\n')
        storeTXT.write('Val:              ' + ', '.join([ format(spaceExt.var(v['var']).getVal()  ,'.3E') for v in tmplist]) + '   {0}\n'.format(snapNumSig))
        storeTXT.write('Err:              ' + ', '.join([ format(spaceExt.var(v['var']).getError(),'.3E') for v in tmplist]) + '   {0}\n'.format(snapNumSig))


        ## flat the cut values
        #varUsed=[ dic['var'] for dic in tmplist ]

        indexs=[ 0 for n in tmplist ]
        cutList=[]
        cutIndx=[]
        #while True:
        #    cc=[ None for c in tmplist ]
        #    writeListContent(cc,indexs,tmplist)
        #    cutList.append(cc)
        #    cutIndx.append([a for a in indexs])
        #    terminate=plusOne(indexs,tmplist)

        #    if terminate:
        #        break
        recIdxList=[1,2]
        for idx,dic in enumerate(tmplist):
            for recIdx in recIdxList:
                # initialized value : mean
                cc=[ val['values'][0] for val in tmplist ]
                indx=[ 0 for n in tmplist ]

                indx[idx] = recIdx
                if idx<len(scanVarList):
                    cc[idx]=tmplist[idx]['values'][recIdx]
                    print 'list array : ' + ''.join( str(a) for a in indx)

                    cutList.append(cc)
                    cutIndx.append(indx)

        # apply cut values and fit to data.
        for i,cut in enumerate(cutList):
            cuttitle=[]
            # fix parameter to specific value
            for ii, dic in enumerate(tmplist):
            #for ii, vName in enumerate(varUsed):
                spaceExt.var(dic['var']).setVal(cut[ii])
                spaceExt.var(dic['var']).setConstant(True)
                cuttitle.append('{name}={var:.3E}'.format(name=dic['title'],var=cut[ii]))

            numSig.setVal(snapNumSig)
            numBkg.setVal(snapNumBkg)
            fitres=model.fitTo(dataset,RooFit.Save(True),RooFit.Minos(useMinos))

            plot=var.frame(RooFit.Title('cuts='+'&&'.join(cuttitle)))
            dataset.plotOn(plot)
            model.plotOn(plot,RooFit.Normalization( dataset.sumEntries(),RooAbsReal.NumEvent))
            SaveResult(
                    origPlot=plot,
                    origVar=var,
                    data={'content':dataset},
                    totPDF={'content':model},
                    fitres=fitres,
                    label=label+'_'+''.join(str(a) for a in cutIndx[i]),
                    fitDir=fitDir,
                    figDir=figDir,
                    absNumNormalize=dataset.sumEntries()
                    )
            storeTXT.write(label+'_'+''.join(str(a) for a in cutIndx[i]) +':'+', '.join([ format(c,'.3E') for c in cut]) + ' yield={0}\n'.format(numSig.getVal()))
    # scan Lb likelihood end }}}

    # scan lB likelihood {{{
    # jack's profile likelihood scan
    if sysFitlB:
        label='syslBFit'

        numSig=spaceExt.var('numlB')
        numBkg=spaceExt.var('numCombBkg_Run2016Data_nLbL0')
        varName='lbl0Mass'
        figDir.cd()

        var=space.var(varName)
        model=space1st.pdf('totPdf_Run2016Data_nLbL0')
        #dataset=model.generate(RooArgSet(space.var('lbtkMass')),10000)
        dataset=loadDatasetlB.reduce('{x}>{minVal}&&{x}<{maxVal}'.format(x=varName,minVal=var.getMin(),maxVal=var.getMax()))
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

        snapNumSig=numSig.getVal()
        snapNumBkg=numBkg.getVal()


        totalVarList=[
                'c1_Run2016Data_nLbL0',
                'c2_Run2016Data_nLbL0',
                ]
        scanVarList=[
                {'var':'frac1_lbloDist_lbloMC', 'title':'frac_sigGaus'},
                {'var':'mean_lbloDist_lbloMC', 'title':'mean_sigGaus'},
                {'var':'sigma_MCfit_lbloDist_lbloMC1', 'title':'width1_sigGaus'},
                {'var':'sigma_MCfit_lbloDist_lbloMC2', 'title':'width2_sigGaus'},
                {'var':'data_MC_factor_lbloDist_lbloMC', 'title':'factor_dataMCFactor'},
                ]

        tmplist=[]
        # record how much variable needs to be scan.
        for varInfo in scanVarList:
            v=spaceExt.var(varInfo['var'])
            VAL=v.getVal()
            ERR=v.getError()
            fitList=[VAL-ERR,VAL,VAL+ERR]
            tmplist.append({'var':varInfo['var'],'values':fitList,'title':varInfo['title']})
        # record the variable not need to be scan.
        for varInfo in totalVarList:
            lostVar=True
            for rec in tmplist:
                if varInfo == rec['var']:
                    lostVar=False
            if lostVar:
                tmplist.append({'var':varInfo,'values':[spaceExt.var(varInfo).getVal()],
                                'title':'constraintTo'+varInfo})
        storeTXT.write('cat:              ' + ', '.join([v['var'] for v in tmplist]) + '\n')
        storeTXT.write('Val:              ' + ', '.join([ format(spaceExt.var(v['var']).getVal()  ,'.3E') for v in tmplist]) + '   {0}\n'.format(snapNumSig))
        storeTXT.write('Err:              ' + ', '.join([ format(spaceExt.var(v['var']).getError(),'.3E') for v in tmplist]) + '   {0}\n'.format(snapNumSig))


        ## flat the cut values
        #varUsed=[ dic['var'] for dic in tmplist ]

        indexs=[ 0 for n in tmplist ]
        cutList=[]
        cutIndx=[]
        #while True:
        #    cc=[ None for c in tmplist ]
        #    writeListContent(cc,indexs,tmplist)
        #    cutList.append(cc)
        #    cutIndx.append([a for a in indexs])
        #    terminate=plusOne(indexs,tmplist)

        #    if terminate:
        #        break
        recIdxList=[1,2]
        for idx,dic in enumerate(tmplist):
            for recIdx in recIdxList:
                # initialized value : mean
                cc=[ val['values'][0] for val in tmplist ]
                indx=[ 0 for n in tmplist ]

                indx[idx] = recIdx
                if idx<len(scanVarList):
                    cc[idx]=tmplist[idx]['values'][recIdx]
                    print 'list array : ' + ''.join( str(a) for a in indx)

                    cutList.append(cc)
                    cutIndx.append(indx)

        # apply cut values and fit to data.
        for i,cut in enumerate(cutList):
            cuttitle=[]
            # fix parameter to specific value
            for ii, dic in enumerate(tmplist):
            #for ii, vName in enumerate(varUsed):
                spaceExt.var(dic['var']).setVal(cut[ii])
                spaceExt.var(dic['var']).setConstant(True)
                cuttitle.append('{name}={var:.3E}'.format(name=dic['title'],var=cut[ii]))

            numSig.setVal(snapNumSig)
            numBkg.setVal(snapNumBkg)
            fitres=model.fitTo(dataset,RooFit.Save(True),RooFit.Minos(useMinos))

            plot=var.frame(RooFit.Title('cuts='+'&&'.join(cuttitle)))
            dataset.plotOn(plot)
            model.plotOn(plot,RooFit.Normalization( dataset.sumEntries(),RooAbsReal.NumEvent))
            SaveResult(
                    origPlot=plot,
                    origVar=var,
                    data={'content':dataset},
                    totPDF={'content':model},
                    fitres=fitres,
                    label=label+'_'+''.join(str(a) for a in cutIndx[i]),
                    fitDir=fitDir,
                    figDir=figDir,
                    absNumNormalize=dataset.sumEntries()
                    )
            storeTXT.write(label+'_'+''.join(str(a) for a in cutIndx[i]) +':'+', '.join([ format(c,'.3E') for c in cut]) + ' yield={0}\n'.format(numSig.getVal()))
    # scan lB likelihood end }}}
    canv.Clear()



canv.SaveAs(tMPfIG+']')
outFile.cd()
space.Write()
outFile.Close()
os.system('mv {0} {1}'.format(tMPrOOTnAME,storeFileName))
os.system('mv {0} {1}'.format(tMPfIG,storeFigName))

txtRecFile.close()
storeTXT.close()
