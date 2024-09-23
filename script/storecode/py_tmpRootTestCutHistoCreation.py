#!/usr/bin/env python

from ROOT import TFile, TNtupleD, TCanvas, TH1D

StorageFolder='store_fig'
filein = TFile.Open('data_treeForCUT.root')
datasets = [
        '2016Data',
        'LbTk',
        'AntiLbTk',
        'AntiBdToJpsiKstar892',
        'AntiBdToJpsiKstar1432',
        'AntiBdToJpsiKpi',
        'AntiBsToJpsiKK',
        'AntiBsToJpsiPhi',
        'AntiBsToJpsiF',
        'BdToJpsiKstar892',
        'BdToJpsiKstar1432',
        'BdToJpsiKpi',
        'BsToJpsiKK',
        'BsToJpsiPhi',
        'BsToJpsiF',
    ]
histNames = {
        "Cutlb":[5.2,7.],
        "vetoCutlb":[5.2,7.],
        "Cutbd":[5.0,5.6],
        "vetoCutbd":[5.0,6.0],
        "Cutbs":[5.0,6.0],
        "vetoCutbs":[5.0,6.0],
    }


## 10MeV per bin
myHists = { myname : TH1D(myname,'NOTITLE', int(100*(myRange[1]-myRange[0])), myRange[0],myRange[1]) for myname, myRange in histNames.iteritems() }


canv=TCanvas('c1','c1',1600,1000)
canv.Divide(2,1)
canv.SetFillColor(4000)
canv.SetFillStyle(4000)
canv.SetFrameFillColor(4000)
canv.SetFrameFillStyle(4000)
pad1=canv.GetPad(1)
pad2=canv.GetPad(2)
pad1.SetFillColor(4000)
pad1.SetFillStyle(4000)
pad2.SetFillColor(4000)
pad2.SetFillStyle(4000)

kpiRange=[0.89-0.05,0.89+0.05]
kkRange=[1.02-0.01,1.02+0.01]
bdRange=[5.28-0.03,5.28+0.03]
bsRange=[5.367-0.02,5.367+0.02]
#vetoBGCut="!(bdMass>5.25&&bdMass<5.3&&kpiMass>0.85&&kpiMass<0.95)&&!(bdbarMass>5.25&&bdbarMass<5.3&&kpibarMass>0.85&&kpibarMass<0.95) && !(bsMass>5.35&&bsMass<5.38&&kkMass>1.015&&kkMass<1.025) && !(kpiMass>1.1&&kpiMass<1.6&&bdMass>5.25&&bdMass<5.3) && !(kpibarMass>1.1&&kpibarMass<1.6&&bdbarMass>5.25&&bdbarMass<5.3) &&lbtkbarMass<8."
vetoBGCut="!(bdMass>{0}&&bdMass<{1}&&kpiMass>{4}&&kpiMass<{5})&&!(bdbarMass>{0}&&bdbarMass<{1}&&kpibarMass>{4}&&kpibarMass<{5}) && !(bsMass>{2}&&bsMass<{3}&&kkMass>{6}&&kkMass<{7})".format(bdRange[0],bdRange[1],bsRange[0],bsRange[1],kpiRange[0],kpiRange[1],kkRange[0],kkRange[1])
poskinematicCut= "lbtkFDsig>10&&tktkCosa2d>0.9&&lbtkCosa2d>0.999&&lbtkVtxProb>0.2&&lbtkFDsig>15.&&tk1Pt>3.&&tk2Pt>2."
negkinematicCut= "lbtkFDsig>10&&tktkCosa2d>0.9&&lbtkCosa2d>0.999&&lbtkVtxProb>0.2&&lbtkFDsig>15.&&tk2Pt>3.&&tk1Pt>2."
tightCut='tktkPt>15.'
lbtkframecut="lbtkMass>{0}&&lbtkMass<{1}".format(histNames['Cutlb'][0],histNames['Cutlb'][1])
lbtkbarframecut="lbtkbarMass>{0}&&lbtkbarMass<{1}".format(histNames['Cutlb'][0],histNames['Cutlb'][1])
bdframecut="bdMass>{0}&&bdMass<{1}".format(histNames['Cutbd'][0],histNames['Cutbd'][1])
bdbarframecut="bdbarMass>{0}&&bdbarMass<{1}".format(histNames['Cutbd'][0],histNames['Cutbd'][1])
bsframecut="bsMass>{0}&&bsMass<{1}".format(histNames['Cutbs'][0],histNames['Cutbs'][1])

pdfTemplateName='sumFig_{0}.pdf'
for dataset in datasets:
    data=filein.Get(dataset)
    if data == None:
        continue
    pdfName=pdfTemplateName.format(dataset)
    canv.SaveAs(pdfName+'[')

    # LbTk mass distribution
    pad1.cd()
    data.Draw('lbtkMass>>Cutlb', '&&'.join([poskinematicCut,lbtkframecut]))
    myHists['Cutlb'].GetXaxis().SetTitle('#Lambda^{0}_{b} mass(GeV)')
    myHists['Cutlb'].SetTitle('#Lambda^{0}_{b} distribution (dataset=%s)' % (dataset))
    pad2.cd()
    data.Draw('lbtkMass>>vetoCutlb', '&&'.join([poskinematicCut,lbtkframecut,vetoBGCut]))
    myHists['vetoCutlb'].GetXaxis().SetTitle('#Lambda^{0}_{b} mass(GeV)')
    myHists['vetoCutlb'].SetTitle('#Lambda^{0}_{b} distribution veto background (dataset=%s)' % (dataset))
    canv.SaveAs('{0}/{1}_LbMassInCut.C'.format(StorageFolder,dataset))
    canv.SaveAs(pdfName)

    # Anti LbTk mass distribution
    pad1.cd()
    data.Draw('lbtkbarMass>>Cutlb', '&&'.join([negkinematicCut,lbtkbarframecut]))
    myHists['Cutlb'].GetXaxis().SetTitle('#bar{#Lambda^{0}_{b}} mass(GeV)')
    myHists['Cutlb'].SetTitle('#bar{#Lambda^{0}_{b}} distribution (dataset=%s)' % (dataset))
    pad2.cd()
    data.Draw('lbtkbarMass>>vetoCutlb', '&&'.join([negkinematicCut,lbtkbarframecut,vetoBGCut]))
    myHists['vetoCutlb'].GetXaxis().SetTitle('#bar{#Lambda^{0}_{b}} mass(GeV)')
    myHists['vetoCutlb'].SetTitle('#bar{#Lambda^{0}_{b}} distribution veto background (dataset=%s)' % (dataset))
    canv.SaveAs('{0}/{1}_AntiLbMassInCut.C'.format(StorageFolder,dataset))
    canv.SaveAs(pdfName)

    # bd Mass distribution
    pad1.cd()
    data.Draw('bdMass>>Cutbd', '&&'.join([poskinematicCut,bdframecut]))
    myHists['Cutbd'].GetXaxis().SetTitle('B^{0}_{d} mass(GeV)')
    myHists['Cutbd'].SetTitle('B^{0}_{d} distribution (dataset=%s)' % (dataset))
    pad2.cd()
    data.Draw('bdMass>>vetoCutbd', '&&'.join([poskinematicCut,bdframecut,vetoBGCut]))
    myHists['vetoCutbd'].GetXaxis().SetTitle('B^{0}_{d} mass(GeV)')
    myHists['vetoCutbd'].SetTitle('B^{0}_{d} distribution veto background (dataset=%s)' % (dataset))
    canv.SaveAs('{0}/{1}_BdMassInCut.C'.format(StorageFolder,dataset))
    canv.SaveAs(pdfName)

    # Anti bd mass distribution
    pad1.cd()
    data.Draw('bdbarMass>>Cutbd', '&&'.join([negkinematicCut,bdbarframecut]))
    myHists['Cutbd'].GetXaxis().SetTitle('#bar{B^{0}_{d}} mass(GeV)')
    myHists['Cutbd'].SetTitle('#bar{B^{0}_{d}}distribution (dataset=%s)' % (dataset))
    pad2.cd()
    data.Draw('bdbarMass>>vetoCutbd', '&&'.join([negkinematicCut,bdbarframecut,vetoBGCut]))
    myHists['vetoCutbd'].GetXaxis().SetTitle('#bar{B^{0}_{d}} mass(GeV)')
    myHists['vetoCutbd'].SetTitle('#bar{B^{0}_{d}} distribution veto background (dataset=%s)' % (dataset))
    canv.SaveAs('{0}/{1}_AntiLbMassInCut.C'.format(StorageFolder,dataset))
    canv.SaveAs(pdfName)

    # bs Mass distribution
    pad1.cd()
    data.Draw('bsMass>>Cutbs', '&&'.join([poskinematicCut,bsframecut]))
    myHists['Cutbs'].GetXaxis().SetTitle('B^{0}_{s} mass(GeV)')
    myHists['Cutbs'].SetTitle('B^{0}_{s} distribution (dataset=%s)' % (dataset))
    pad2.cd()
    data.Draw('bsMass>>vetoCutbs', '&&'.join([poskinematicCut,bsframecut,vetoBGCut]))
    myHists['vetoCutbs'].GetXaxis().SetTitle('B^{0}_{s} mass(GeV)')
    myHists['vetoCutbs'].SetTitle('B^{0}_{s} distribution veto background (dataset=%s)' % (dataset))
    canv.SaveAs('{0}/{1}_BdMassInCut.C'.format(StorageFolder,dataset))
    canv.SaveAs(pdfName)

    canv.SaveAs(pdfName+']')


