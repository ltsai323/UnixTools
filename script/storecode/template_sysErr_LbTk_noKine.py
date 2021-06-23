#!/usr/bin/env python

import os
from array import array
from ROOT import TLegend, TBox, TLine
from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataSet, RooDataHist, RooArgSet, RooArgList, TGaxis, TPad, TLine, TGraphErrors, TGraph, gRandom, TNtupleD
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooGenericPdf, RooCategory, RooSimultaneous,RooMsgService, RooAbsData, RooPlot, RooAbsReal, RooExtendPdf, RooMinuit
import time











#dataFileName='result_flatNtuple_NoSelection.root'
dataFileName='result_flatNtuple_LbTk_preSelection_noKinematicCut.root'
#dataFileName='result_flatNtuple_LbTk_preSelection_withKinematicCut.root'
storeFileName='store_root/workspace_extraStep_3rd_LbTk_sysmaticErrFit_noKinematicCut_{0}.root'.format(ptRange)
storeFigName ='store_fig/pdf_workspace_extraStep_3rd_LbTk_sytematicErrFit_noKinematicCut_{0}.pdf'.format(ptRange)
storeTXTName='log_workspace_extraStep_3rd_LbTk_sytematicErrFit_noKinematicCut_{0}.txt'.format(ptRange)
storeTXT=open(storeTXTName,'w')

tMPrOOTnAME='tmp.root'
tMPfIG='tmp.pdf'
currenttime=time.time()
rectime=currenttime


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


# used for find flat cut values
def plusOne(L,Ls,idx=0):
    # if add 
    #print('plusOne:: idx={0}, L={1}, Ls[idx]={2}'.format(idx,L,Ls[idx]))
    if L[idx]+1 == len(Ls[idx]['values']):
        L[idx]=0
        j=idx+1

        # terminate whole while loop.
        if j == len(L):
            #print('plusOne:: idx={0} hihihi'.format(j))
            return True

        # iterate function
        return plusOne(L,Ls,j)
    else:
        # main function to add one.
        L[idx]+=1
        return False
def writeListContent(recList,indexs,content):
    for i,idx in enumerate(indexs):
        #print 'i,idx[i] = {0}, {1}'.format(i,idx)
        #print '  content[i] = {0}'.format(content[i])
        #print '    recList[i] = {0}'.format(recList[i])
        #print '      content[i][values] = {0}'.format(content[i]['values'])
        aaa=content[i]
        #recList[i]=content[i]['values'][idx]
        recList[i]=aaa['values'][idx]
# used for find flat cut values end
# def functions end }}}

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
#workspaceFileE=TFile.Open('store_root/workspace_extraStep_1st_noSelectionLbFit.root')
workspaceFileE=TFile.Open('store_root/workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.root')
#workspaceFileE=TFile.Open('store_root/workspace_extraStep_1st_shortRangeLbFit_withKinematicCut.root')
spaceExt=workspaceFileE.Get('space')
spaceExt.SetName('spaceExt')


load2016Data=True
if load2016Data:
    sysFitLb=True
    sysFitlB=True
    inFile16=TFile.Open(dataFileName)
    inN16=inFile16.Get('pLbTk/2016Data')
    inn16=inFile16.Get('nLbTk/2016Data')

    # load parameters from other workspace and import them in current workspace
    massLb=space.var('lbtkMass')
    masslB=space.var('lbtkbarMass')


    massLb.setBins(50)
    masslB.setBins(50)

    massLb.setRange('sigRangeLb',5.4,5.9)
    masslB.setRange('sigRangelB',5.4,5.9)

    loadDatasetLb=RooDataSet('loadDatasetLb','loadData16',inN16,RooArgSet(massLb,space.var('lbtkPt')))
    loadDatasetlB=RooDataSet('loadDatasetlB','loadData16',inn16,RooArgSet(masslB,space.var('lbtkPt')))
    totNum=loadDatasetLb.sumEntries()
    space.factory('numLb[{0},-1000.,{1}]'.format(space2nd.var('numLb').getVal(),totNum))
    space.factory('numlB[{0},0.,{1}]'.format(2000.,totNum))

    simulComponents=[]

    # find systematic of Lb {{{
    if sysFitLb:
        label='LbSysFit'

        numSig=spaceExt.var('numLb')
        numBkg=spaceExt.var('numCombBkg_ShortRangeLbFit')
        varName='lbtkMass'
        figDir.cd()

        var=space.var(varName)
        model=spaceExt.pdf('totPdf_LbModel')
        #dataset=model.generate(RooArgSet(space.var('lbtkMass')),10000)
        dataset=loadDatasetLb.reduce(ptCut)
        nll=model.createNLL(dataset)
        fitres=model.fitTo(dataset,RooFit.Save(True),RooFit.Minos(useMinos))


        plot=var.frame(RooFit.Title('toyMC check fit'))
        dataset.plotOn(plot)
        model.plotOn(plot,RooFit.Normalization( dataset.sumEntries(),RooAbsReal.NumEvent))
        SaveResult(
                origPlot=plot,
                origVar=var,
                data={'content':dataset},
                totPDF={'content':model},
                fitres=fitres,
                label=label+'resFitCheck_data',
                fitDir=fitDir,
                figDir=figDir,
                absNumNormalize=dataset.sumEntries()
                )

        snapNumSig=numSig.getVal()
        snapNumBkg=numBkg.getVal()



        totalVarList=[
                'cp1',
                'cp2',
                'cp3',
                ]
        scanVarList=[
                {'var':'frac_lbtkDist_lbtkMC1', 'title':'frac_sigGaus'},
                {'var':'mu_lbtkDist_lbtkMC', 'title':'mean_sigGaus'},
                {'var':'sigma_MC_lbtkDist_lbtkMC1', 'title':'width1_sigGaus'},
                {'var':'sigma_MC_lbtkDist_lbtkMC2', 'title':'width2_sigGaus'},
                {'var':'bsMultiplier', 'title':'factor_dataMCFactor'},
                ]

        tmplist=[]
        # record how much variable needs to be scan.
        # values: 0.mean, 1.mean-err, 2.mean+err
        for varInfo in scanVarList:
            v=spaceExt.var(varInfo['var'])
            VAL=v.getVal()
            ERR=v.getError()
            #fitList=[VAL-ERR,VAL,VAL+ERR]
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
        storeTXT.write('Val:              ' + ', '.join([ format(spaceExt.var(v['var']).getVal()  ,'.3E') for v in tmplist]) + '{0}\n'.format(snapNumSig))
        storeTXT.write('Err:              ' + ', '.join([ format(spaceExt.var(v['var']).getError(),'.3E') for v in tmplist]) + '{0}\n'.format(snapNumSig))


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

            plot=var.frame(RooFit.Title('cuts='+'&&'.join( str(a) for a in cuttitle)))
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
            storeTXT.write(label+'_'+''.join(str(a) for a in cutIndx[i]) +':'+', '.join([ format(c,'.3E') for c in cut]) + 'yield={0}\n'.format(numSig.getVal()))
    # find systematic error of Lb end }}}
    # find systematic of lB {{{
    if sysFitlB:
        label='lBSysFit'

        numSig=spaceExt.var('numlB')
        numBkg=spaceExt.var('numCombBkg_ShortRangelBFit')
        varName='lbtkbarMass'
        figDir.cd()

        var=space.var(varName)
        model=spaceExt.pdf('totPdf_lBModel')
        #dataset=model.generate(RooArgSet(space.var('lbtkMass')),10000)
        dataset=loadDatasetlB.reduce(ptCut)
        fitres=model.fitTo(dataset,RooFit.Save(True),RooFit.Minos(useMinos))


        plot=var.frame(RooFit.Title('toyMC check fit'))
        dataset.plotOn(plot)
        model.plotOn(plot,RooFit.Normalization( dataset.sumEntries(),RooAbsReal.NumEvent))
        SaveResult(
                origPlot=plot,
                origVar=var,
                data={'content':dataset},
                totPDF={'content':model},
                fitres=fitres,
                label=label+'resFitCheck_data',
                fitDir=fitDir,
                figDir=figDir,
                absNumNormalize=dataset.sumEntries()
                )

        snapNumSig=numSig.getVal()
        snapNumBkg=numBkg.getVal()



        totalVarList=[
                'cp1_',
                'cp2_',
                'cp3_',
                ]
        scanVarList=[
                {'var':'frac_lbtkbarDist_antilbtkMC1', 'title':'frac_sigGaus'},
                {'var':'mu_lbtkbarDist_antilbtkMC', 'title':'mean_sigGaus'},
                {'var':'sigma_MC_lbtkbarDist_antilbtkMC1', 'title':'width1_sigGaus'},
                {'var':'sigma_MC_lbtkbarDist_antilbtkMC2', 'title':'width2_sigGaus'},
                {'var':'bsMultiplier', 'title':'factor_dataMCFactor'},
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
        storeTXT.write('Val:              ' + ', '.join([ format(spaceExt.var(v['var']).getVal()  ,'.3E') for v in tmplist]) + '{0}\n'.format(snapNumSig))
        storeTXT.write('Err:              ' + ', '.join([ format(spaceExt.var(v['var']).getError(),'.3E') for v in tmplist]) + '{0}\n'.format(snapNumSig))


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
            storeTXT.write(label+'_'+''.join(str(a) for a in cutIndx[i]) +':'+', '.join([ format(c,'.3E') for c in cut]) + 'yield={0}\n'.format(numSig.getVal()))
    # find systematic error of lB end }}}


    canv.Clear()


canv.SaveAs(tMPfIG+']')
outFile.cd()
space.Write()
outFile.Close()
os.system('mv {0} {1}'.format(tMPrOOTnAME,storeFileName))
os.system('mv {0} {1}'.format(tMPfIG,storeFigName))

storeTXT.close()
