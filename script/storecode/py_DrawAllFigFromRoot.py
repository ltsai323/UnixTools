#!/usr/bin/env python2
from ROOT import TFile,TCanvas,TIter,TKey
from ROOT import RooPlot, RooFit

pdf='check.pdf'

file=TFile.Open('store_root/workspace_1stStep_MCShape.root')
dir=file.Get('figs')
l=dir.GetListOfKeys()
canv=TCanvas('c1','',2000,1500)
canv.SetFillStyle(4000)
canv.SetFillColor(4000)
canv.Update()
canv.SaveAs(pdf+'[')
for key in l:
    n=key.GetName()
    obj=dir.Get(n)
    #obj.GetXaxis().SetRangeUser(5.1,7.)
    print obj.GetName()
    obj.Draw()
    canv.SaveAs('fit_'+n+'.pdf')
    canv.SaveAs(pdf)
canv.SaveAs(pdf+']')
