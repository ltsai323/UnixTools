#!/usr/bin/env python2

from ROOT import TFile, TNtuple, TH1D, TCanvas, TLorentzVector, TChain
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgSet, RooArgList, RooTreeData
from ROOT import RooPlot

def lbMassFit( importedDataSet, lbMassVar ):
    dataWithCut=fitdata.reduce( RooFit.Cut("tktkPt>2.") )

    sigpar_mean =RooRealVar('sig_gau{0}_mean'.format(1), 'parameter to gaussian{0}: mean'.format(1), 5.637, 5.0, 6.0)
    sigpar_width=RooRealVar('sig_gau{0}_width'.format(1), 'parameter to gaussian{0}: width'.format(1), 0.01, 0.000000001, 10.)
    sigpdf_gaus =RooRealVar('sig_gau{0}_pdf'.format(1), 'pdf : gaussian{0}', lbMassVar, sigpar_mean, sigpar_width )

    bkgpar1     =RooRealVar('bkg_par1', 'parameter to chebychev : 1st', 0.5, -10., 10. )
    bkgpar2     =RooRealVar('bkg_par2', 'parameter to chebychev : 2nd',-0.2, -10., 10. )
    bkgpar3     =RooRealVar('bkg_par3', 'parameter to chebychev : 3rd',-0.2, -10., 10. )









from array import array
if __name__ == "__main__":
    ipFile=TFile('result_flatNtuple_2016RunB2CDFG.root')
    ntuple=ipFile.Get('root')

    lbtkMass=RooRealVar('lbtkMass', 'lbtkMass', 5.6, 4.5, 8.0, "GeV")
    bsMass=RooRealVar('bsMass', 'bsMass', 4., 8., "GeV")
    bdMass=RooRealVar('bdMass', 'bdMass', 3.5, 8., "GeV")
    bdbarMass=RooRealVar('bdbarMass', 'bdbarMass', 3.5, 8., "GeV")

    phiMass=RooRealVar('phiMass', 'phiMass', 0.5, 3., "GeV")
    kstarMass=RooRealVar('kstarMass', 'kstarMass', 0.5, 3., "GeV")
    kstarbarMass=RooRealVar('kstarbarMass', 'kstarbarMass', 0.5, 3., "GeV")


    tktkPt=RooRealVar('tktkPt', 'tktkPt', 0.,  160., "GeV/c")

    fitMC=RooDataSet()
    fitdata=RooDataSet('2016Data', 'RunB', ntuple, RooArgSet(lbtkMass,bsMass,bdMass,bdbarMass,phiMass,kstarMass,kstarbarMass,tktkPt))


    subdataset=fitdata.reduce( RooFit.Cut("tktkPt>20.&&lbtkMass>5.45&&lbtkMass<5.8") )
    canv=TCanvas('c1', 'c1', 1600,1000)
    canv.SetFillColor(4000)
    canv.SetFillStyle(4000)
    lbtkmassFrame=lbtkMass.frame(RooFit.Range(5.,6.))
    bsmassFrame=bsMass.frame(RooFit.Range(5.,6.))
    bdmassFrame=bdMass.frame(RooFit.Range(5.,6.))
    bdbarmassFrame=bdbarMass.frame(RooFit.Range(5.,6.))

    fitdata.plotOn(lbtkmassFrame, RooFit.Cut("tktkPt>20."))
    subdataset.plotOn(bsmassFrame)
    subdataset.plotOn(bdmassFrame)
    subdataset.plotOn(bdbarmassFrame)

    lbtkmassFrame.Draw()
    canv.SaveAs('h_checkPlot_lbtkMass_tktkPtB20.eps')
    bsmassFrame.Draw()
    canv.SaveAs('h_checkPlot_BsMass_lbtkCriticalRegion_tktkPtB20.eps')
    bdmassFrame.Draw()
    canv.SaveAs('h_checkPlot_BdMass_lbtkCriticalRegion_tktkPtB20.eps')
    bdbarmassFrame.Draw()
    canv.SaveAs('h_checkPlot_BdBarMass_lbtkCriticalRegion_tktkPtB20.eps')

