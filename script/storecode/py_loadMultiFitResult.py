#!/usr/bin/env python2

from ROOT import TFile, TH1D, TKey, TIter
from ROOT import RooFit


fileIn=TFile.Open('store_root/workspace_extraStep_3rd_sysmaticErrFit_noKinematicCut.root')
dir=fileIn.Get('fitRes')
print dir

next=TIter(dir.GetListOfKeys())
key=(TKey)next()
while key:
    key=(TKey)next()
    print 'hi'

#next=fileIn.Get

