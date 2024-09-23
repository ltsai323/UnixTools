#!/usr/bin/env python

from ROOT import TFile, TH1F, TH1D, TCanvas, RooRealVar, RooDataHist, RooArgSet, RooArgList
from ROOT import RooGaussian, RooAddPdf, RooPolynomial, RooExponential, RooCBShape, RooArgusBG, RooFit, RooWorkspace, RooDataSet



if __name__ == '__main__':
    datasetNames=[
            '2016Data',
           # 'AntiLbTk',
           # 'AntiBdToJpsiKstar892',
           # 'AntiBdToJpsiKstar1432',
           # 'AntiBdToJpsiKpi',
           # 'AntiBsToJpsiKK',
           ##'AntiBsToJpsiPhi',
           # 'AntiBsToJpsiF',
           # 'LbTk',
           # 'BdToJpsiKstar892',
           # 'BdToJpsiKstar1432',
           # 'BdToJpsiKpi',
           # 'BsToJpsiKK',
           ##'BsToJpsiPhi',
           # 'BsToJpsiF',
            ]
    vars={
            'lbtkMass':		[  5.1,  7.0],
            'lbtkPt':		[  00., 100.],
            'lbtkbarMass':	[  00., 100.],
            'mumuMass':		[  00., 100.],
            'mumuPt':		[  00., 100.],
            'tktkMass':		[  00., 100.],
            'tktkPt':		[  00., 100.],
            'bsMass':		[  00., 100.],
            'kkMass':		[  00., 100.],
            'bdMass':		[  00., 100.],
            'kpiMass':		[  00., 100.],
            'bdbarMass':	[  00., 100.],
            'kpibarMass':	[  00., 100.],
            }


    # open file
    fIn=TFile.Open('result_flatNtuple.root')

    # load ntuples from file
    loadedNtuple={ dName : fIn.Get(dName) for dName in datasetNames }

    # create workspace
    space=RooWorkspace('thespace',False)

    # dict for RooRealVar from vars
    datavars={}
    for varName, varRange in vars.iteritems():
        space.factory( '{0}[{1},{2}]'.format(varName,varRange[0],varRange[1]) )

        # 5MeV per bin.
        space.var(varName).setBins( int((varRange[1]-varRange[0])*200) )
        datavars.update( {varName:space.var(varName)} )

    # dict for RooDataSet from loaded Ntuples
    unbinDatas={}
    for dsetName in datasetNames:
        if loadedNtuple[dsetName] == None:
            continue
        unbinDatas.update(
                {
                    dsetName:RooDataSet(
                        dsetName,
                        dsetName,
                        RooArgSet(
                            datavars['lbtkMass'],
                            datavars['lbtkPt'],
                            datavars['lbtkbarMass'],
                            #datavars['mumuMass'],
                            #datavars['mumuPt'],
                            #datavars['tktkMass'],
                            #datavars['tktkPt'],
                            #datavars['bsMass'],
                            #datavars['kkMass'],
                            #datavars['bdMass'],
                            #datavars['kpiMass'],
                            #datavars['bdbarMass'],
                            #datavars['kpibarMass'],
                        ),
                        RooFit.Import(loadedNtuple[dsetName])
                    )
                }
            )

    # create histograms.
    histos={}
    for dName, dataset in unbinDatas.iteritems():
        hists={}
        hists.update({
            'lbtkMass':
            RooDataHist(
                '%s_%s'%(dName,'lbtkMass'),
                'lbtkMass distribution in %s'%(dName),
                RooArgSet(datavars['lbtkMass']),
                dataset
                )
            })
        hists['lbtkMass'].Print('v')


        histos.update({dName:hists})




    # create combinatorial bkg PDF. exp(-x/(c1+c2))-exp(-x/c1)
    space.factory('EXPR::cBKG( "( exp(-1.*(lbtkMass-mShift)/(cPar1+cPar2)) - exp(-1.*(lbtkMass-mShift)/cPar1) )", lbtkMass, mShift[4.8,0.1,10.0], cPar1[0.44,0.001,100.],cPar2[0.0025,0.0000001,10.] )')
    cBKG=space.pdf('cBKG')

    canv=TCanvas('c1','c1',1600,1000)
    canv.SaveAs('firstCheck.pdf[')
    for dName, hists in histos.iteritems():
        cBKG.fitTo(hists['lbtkMass'])
        cBKG.fitTo(hists['lbtkMass'])

        frame=datavars['lbtkMass'].frame()
        hists['lbtkMass'].plotOn(frame)
        cBKG.plotOn(frame)

        frame.Draw()
        canv.SaveAs('firstCheck.pdf')
    canv.SaveAs('firstCheck.pdf]')




