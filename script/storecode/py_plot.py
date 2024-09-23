#!/usr/bin/env python2
figFolder='storefig'
pdfFile='{}/tot.pdf'.format(figFolder)


from ROOT import TFile
from ROOT import TCanvas
from ROOT import TH1D
from ROOT import TPaveText

rootFile=TFile.Open('storeroot/tree_vertexProducer_2016RunBCDEFGH_HLTRecord.root')

plbl0=rootFile.Get('VertexCompCandAnalyzer/pLbL0')
nlbl0=rootFile.Get('VertexCompCandAnalyzer/nLbL0')
plbtk=rootFile.Get('VertexCompCandAnalyzer/pLbTk')
nlbtk=rootFile.Get('VertexCompCandAnalyzer/nLbTk')

lbl0Cut='tktkMass>1.115-0.010&&tktkMass<1.115+0.010&&tktkFlightDistanceSig>10.&&tktkCosa2d>0.9'
canv=TCanvas('c1','c1',1600,1200)
canv.SaveAs(pdfFile+'[')
h_plbl0=TH1D('plbl0','plbl0', 80, 5.4, 5.8)
plbl0.Draw('lbtkMass>>plbl0',lbl0Cut)
h_plbl0.Draw()
canv.SaveAs('{}/h_{}.eps'.format(figFolder,'plbl0Mass'))
canv.SaveAs(pdfFile)

h_nlbl0=TH1D('nlbl0','nlbl0', 80, 5.4, 5.8)
plbl0.Draw('lbtkMass>>nlbl0',lbl0Cut)
h_nlbl0.Draw()
canv.SaveAs('{}/h_{}.eps'.format(figFolder,'nlbl0Mass'))
canv.SaveAs(pdfFile)

h_lbl0=TH1D('pnlbl0','lbl0', 80, 5.4, 5.8)
h_lbl0.Add(h_plbl0)
h_lbl0.Add(h_nlbl0)
h_lbl0.SetStats(False)
h_lbl0.SetTitle('#Lambda^{0}#rightarrow J/#psi #Lambda^{0} Mass')
h_lbl0.GetXaxis().SetTitle('M_{#Lambda^{0}_{b}}(GeV)')
h_lbl0.GetYaxis().SetTitle('event/10MeV')
h_lbl0.SetMaximum(h_lbl0.GetMaximum()*1.7)
h_lbl0.SetMinimum(0.)
h_lbl0.Draw()
## start to calculate sideband substraction
M=0
binRec=0.
for i in range(1,80):
    if h_lbl0.GetBinContent(i) > M:
        M = h_lbl0.GetBinContent(i)
        binRec=i
centreVal=5.619
interval=0.04
minBin=0
maxBin=0
for i in range(1,80):
    if h_lbl0.GetBinCenter(i) < centreVal-interval:
        if h_lbl0.GetBinCenter(i+1) >= centreVal-interval:
            minBin=i
    if h_lbl0.GetBinCenter(i) < centreVal+interval:
        if h_lbl0.GetBinCenter(i+1) >= centreVal+interval:
            maxBin=i
if maxBin-minBin%2 != 0:
    maxBin+=1
sumSig=0
sumSid=0
for num in range(minBin,maxBin+1):
    sumSig+=h_lbl0.GetBinContent(num)
for num in range((3*minBin-maxBin)/2-5, minBin-5+1):
    sumSid+=h_lbl0.GetBinContent(num)
for num in range(maxBin+5,(3*maxBin-minBin)/2+5+1):
    sumSid+=h_lbl0.GetBinContent(num)
print '{} {}'.format(minBin, maxBin)
print '{} {} {}'.format(sumSig, sumSid, 0)
nSIG=float(sumSig-sumSid)
nERR=(float(sumSig))**0.5

texts=TPaveText(0.41,0.70,0.85,0.85,"NDC")
texts.AddText("#frac{{N_{{sig}}}}{{#sigma}}=#frac{{{0:.2f}}}{{{1:.2f}}}={2:.2f}".format(nSIG,nERR,nSIG/nERR))
texts.SetFillStyle(4000)
texts.SetFillColor(4000)
texts.Draw('same')

## end to calculate sideband substraction
canv.SaveAs('{}/h_{}.eps'.format(figFolder,'lbl0Mass_tot'))
canv.SaveAs(pdfFile)

###################################################
concreteCut='tk1Pt>1.6&&tk2Pt>1.0&&lbtkVtxprob>0.05'
testCut='lbtknChi2'
###################################################
h_plbtk=TH1D('plbtk','lbtk',80,5.4,5.8)
plbtk.Draw('lbtkMass>>plbtk',concreteCut)
h_plbtk.SetTitle('lbtk total')
h_plbtk.SetStats(False)
h_plbtk.Draw()



canv.SaveAs('{}/h_{}.eps'.format(figFolder,'plbtkMass'))
canv.SaveAs(pdfFile)

h_plbtk_t1=TH1D('plbtk_t1','lbtk',80,5.4,5.8)
plbtk.Draw('lbtkMass>>plbtk_t1','{}&&{}<{}'.format(concreteCut,testCut,0.1))
h_plbtk_t1.SetTitle('lbtk test1')
canv.SaveAs('{}/h_{}.eps'.format(figFolder,'plbtkMass_test1'))
canv.SaveAs(pdfFile)

h_plbtk_t2=TH1D('plbtk_t2','lbtk',80,5.4,5.8)
plbtk.Draw('lbtkMass>>plbtk_t2','{}&&{}>{}'.format(concreteCut,testCut,0.1))
h_plbtk_t2.SetTitle('lbtk test2')
canv.SaveAs('{}/h_{}.eps'.format(figFolder,'plbtkMass_test2'))
canv.SaveAs(pdfFile)


canv.SaveAs(pdfFile+']')
