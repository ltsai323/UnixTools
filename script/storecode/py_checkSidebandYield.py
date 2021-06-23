#!/usr/bin/env python2

from ROOT import TFile, RooFit, RooWorkspace, RooRealVar, RooPolynomial, RooAbsReal, RooArgSet
import csv

LbL0FileList=[
        { 'range': '20To30', 'file': 'store_root/workspace_0thStep_LbL0Shape_noKinematicCut.ptRange20.30.root',},
        { 'range': '30To33', 'file': 'store_root/workspace_0thStep_LbL0Shape_noKinematicCut.ptRange30.33.root',},
        { 'range': '33To38', 'file': 'store_root/workspace_0thStep_LbL0Shape_noKinematicCut.ptRange33.38.root',},
        { 'range': '38To45', 'file': 'store_root/workspace_0thStep_LbL0Shape_noKinematicCut.ptRange38.45.root',},
        { 'range': '45Tinf', 'file': 'store_root/workspace_0thStep_LbL0Shape_noKinematicCut.ptRange45.root',},
        ]
LbTkFileList=[
        { 'range': '20To30', 'file': 'store_root/workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.ptRange20.30.root',},
        { 'range': '30To33', 'file': 'store_root/workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.ptRange30.33.root',},
        { 'range': '33To38', 'file': 'store_root/workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.ptRange33.38.root',},
        { 'range': '38To45', 'file': 'store_root/workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.ptRange38.45.root',},
        { 'range': '45Tinf', 'file': 'store_root/workspace_extraStep_1st_shortRangeLbFit_noKinematicCut.ptRange45.root',},
        ]
signalRegion=[5.54,5.70]

def checkYield(**kwargs):
    iF=TFile.Open(kwargs['fileName'])
    space=iF.Get('space')

    mass=space.var(kwargs['mass'])
    bkgY=space.var(kwargs['bkgYield'])
    mean=space.var(kwargs['meanVar'])
    wid1=space.var(kwargs['widthVar1'])
    wid2=space.var(kwargs['widthVar2'])
    wid=wid1 if wid1.getVal()>wid2.getVal() else wid2
    bkg=space.pdf(kwargs['bkgPdf'])

    mass.setRange('lSide', mass.getMin()                 , mean.getVal()-2.0*wid.getVal())
    mass.setRange('rSide', mean.getVal()+2.0*wid.getVal(), mass.getMax()                 )

    bkgSideRatio=bkg.createIntegral(RooArgSet(mass),RooFit.NormSet(RooArgSet(mass)),RooFit.Range('lSide,rSide'))

    yVal=bkgY.getVal()
    yErr2=bkgY.getError()**2 # err square
    rVal=bkgSideRatio.getVal()
    rErr2=(rVal*(1-rVal))/yVal # binomial error

    outVal=rVal*yVal
    outErr=(rVal**2*yErr2+rErr2*yVal**2)**0.5
    return ( int(outVal), int(outErr) )
def checkYieldFixSideband(**kwargs):
    iF=TFile.Open(kwargs['fileName'])
    print iF
    space=iF.Get('space')

    mass=space.var(kwargs['mass'])
    bkgY=space.var(kwargs['bkgYield'])
    bkg=space.pdf(kwargs['bkgPdf'])

    # kill mass range
    mass.setRange('lSide', mass.getMin()                     , signalRegion[0]                   )
    mass.setRange('rSide', signalRegion[1]                   , mass.getMax()                     )

    # kill -2sig~2sig
    #mass.setRange('lSide', mass.getMin()                     , kwargs['mean']-2.0*kwargs['width'])
    #mass.setRange('rSide', kwargs['mean']+2.0*kwargs['width'], mass.getMax()                     )

    # keep +-5.5sig~+-3.0sig
    #mass.setRange('lSide', kwargs['mean']-5.5*kwargs['width'], kwargs['mean']-3.0*kwargs['width'])
    #mass.setRange('rSide', kwargs['mean']+3.0*kwargs['width'], kwargs['mean']+5.5*kwargs['width'])

    bkgSideRatio=bkg.createIntegral(RooArgSet(mass),RooFit.NormSet(RooArgSet(mass)),RooFit.Range('lSide,rSide'))
    yVal=bkgY.getVal()
    yErr2=bkgY.getError()**2 # err square
    rVal=bkgSideRatio.getVal()
    rErr2=(rVal*(1-rVal))/yVal # binomial error

    outVal=rVal*yVal
    outErr=(rVal**2*yErr2+rErr2*yVal**2)**0.5
    return ( int(outVal), int(outErr) )

def checkLbL0Yield(fName,sidebandInfo):
    return checkYieldFixSideband(
            fileName=fName,
            mass='lbl0Mass',
            bkgYield='numCombBkg_Run2016Data_pLbL0',
            mean=sidebandInfo[0],
            width=sidebandInfo[1],
            bkgPdf='pPDF_Run2016Data_pLbL0',
            )
    #return checkYield(
    #        fileName=fName,
    #        mass='lbl0Mass',
    #        bkgYield='numCombBkg_Run2016Data_pLbL0',
    #        meanVar='mean_lbl0Dist_lbl0MC',
    #        widthVar1='sigma_MCfit_lbl0Dist_lbl0MC1',
    #        widthVar2='sigma_MCfit_lbl0Dist_lbl0MC2',
    #        bkgPdf='pPDF_Run2016Data_pLbL0',
    #        )
def checklBLoYield(fName,sidebandInfo):
    return checkYieldFixSideband(
            fileName=fName,
            mass='lbl0Mass',
            bkgYield='numCombBkg_Run2016Data_nLbL0',
            mean=sidebandInfo[0],
            width=sidebandInfo[1],
            bkgPdf='pPDF_Run2016Data_nLbL0',
            )
    #return checkYield(
    #        fileName=fName,
    #        mass='lbl0Mass',
    #        bkgYield='numCombBkg_Run2016Data_nLbL0',
    #        meanVar='mean_lbloDist_lbloMC',
    #        widthVar1='sigma_MCfit_lbloDist_lbloMC1',
    #        widthVar2='sigma_MCfit_lbloDist_lbloMC1',
    #        bkgPdf='pPDF_Run2016Data_nLbL0',
    #        )
def checkLbTkYield(fName,sidebandInfo):
    return checkYieldFixSideband(
            fileName=fName,
            mass='lbtkMass',
            bkgYield='numCombBkg_ShortRangeLbFit',
            mean=sidebandInfo[0],
            width=sidebandInfo[1],
            bkgPdf='pPDF_ShortRangeLbFit',
            )
    #return checkYield(
    #        fileName=fName,
    #        mass='lbtkMass',
    #        bkgYield='numCombBkg_ShortRangeLbFit',
    #        meanVar='mu_lbtkDist_lbtkMC',
    #        widthVar1='sigma_MC_lbtkDist_lbtkMC1',
    #        widthVar2='sigma_MC_lbtkDist_lbtkMC2',
    #        bkgPdf='pPDF_ShortRangeLbFit',
    #        )
def checklBTkYield(fName,sidebandInfo):
    return checkYieldFixSideband(
            fileName=fName,
            mass='lbtkbarMass',
            bkgYield='numCombBkg_ShortRangelBFit',
            mean=sidebandInfo[0],
            width=sidebandInfo[1],
            bkgPdf='pPDF_ShortRangelBFit',
            )
    #return checkYield(
    #        fileName=fName,
    #        mass='lbtkbarMass',
    #        bkgYield='numCombBkg_ShortRangelBFit',
    #        meanVar='mu_lbtkbarDist_antilbtkMC',
    #        widthVar1='sigma_MC_lbtkbarDist_antilbtkMC1',
    #        widthVar2='sigma_MC_lbtkbarDist_antilbtkMC2',
    #        bkgPdf='pPDF_ShortRangelBFit',
    #        )

# return a tuple, [0]: mean, [1]: error
def returnSidebandInfo(fName,**kwargs):
    iF=TFile.Open(fName)
    space=iF.Get('space')

    mean=space.var(kwargs['meanVar'])
    wid1=space.var(kwargs['widthVar1'])
    wid2=space.var(kwargs['widthVar2'])
    wid=wid1 if wid1.getVal()>wid2.getVal() else wid2
    return (mean.getVal(),wid.getVal())

writeColumn=[
        'channel',
        '20To30Val','20To30Err',
        '30To33Val','30To33Err',
        '33To38Val','33To38Err',
        '38To45Val','38To45Err',
        '45TinfVal','45TinfErr',
        ]
columnIdx={ name:idx for idx,name in enumerate(writeColumn) }


if __name__ == '__main__':
    ft=open('log_calcSideband_fromFittedBackgroundShape.txt','w')
    fc=open('log_calcSideband_fromFittedBackgroundShape.csv','w')
    cwrite=csv.writer(fc)
    cwrite.writerow(writeColumn)
    LbRec=[ None for i in writeColumn ]
    lBRec=[ None for i in writeColumn ]

    sidebandInfo=returnSidebandInfo(LbTkFileList[0]['file'],
        meanVar='mu_lbtkbarDist_antilbtkMC',
        widthVar1='sigma_MC_lbtkbarDist_antilbtkMC1',
        widthVar2='sigma_MC_lbtkbarDist_antilbtkMC2',
        )
    for fDict in LbTkFileList:
        LbRec[0]='pLbTk'
        fName=fDict['file']
        rName=fDict['range']
        bkgYield=checkLbTkYield(fName,sidebandInfo)
        ft.write('pLbTk sideband in range {1}, (yield,error) = {0}\n'.format(bkgYield, rName) )
        LbRec[ columnIdx[rName+'Val'] ]=bkgYield[0]
        LbRec[ columnIdx[rName+'Err'] ]=bkgYield[1]

        lBRec[0]='nLbTk'
        bkgYield=checklBTkYield(fName,sidebandInfo)
        ft.write('nLbTk sideband in range {1}, (yield,error) = {0}\n'.format(bkgYield, rName) )
        lBRec[ columnIdx[rName+'Val'] ]=bkgYield[0]
        lBRec[ columnIdx[rName+'Err'] ]=bkgYield[1]
    cwrite.writerow(LbRec)
    cwrite.writerow(lBRec)
    for fDict in LbL0FileList:
        LbRec[0]='pLbL0'
        fName=fDict['file']
        rName=fDict['range']
        bkgYield=checkLbL0Yield(fName,sidebandInfo)
        ft.write('pLbL0 sideband in range {1}, (yield,error) = {0}\n'.format(bkgYield, rName) )
        LbRec[ columnIdx[rName+'Val'] ]=bkgYield[0]
        LbRec[ columnIdx[rName+'Err'] ]=bkgYield[1]

        lBRec[0]='nLbL0'
        bkgYield=checklBLoYield(fName,sidebandInfo)
        ft.write('nLbL0 sideband in range {1}, (yield,error) = {0}\n'.format(bkgYield, rName) )
        lBRec[ columnIdx[rName+'Val'] ]=bkgYield[0]
        lBRec[ columnIdx[rName+'Err'] ]=bkgYield[1]
    cwrite.writerow(LbRec)
    cwrite.writerow(lBRec)
    ft.close()
    fc.close()
