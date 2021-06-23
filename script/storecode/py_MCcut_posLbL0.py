#!/usr/bin/env python2
figFolder='store_fig'
pdfFile='{}/tot.pdf'.format(figFolder)


from ROOT import TFile
from ROOT import TCanvas
from ROOT import TH1D
from ROOT import TPaveText

rootFile=TFile.Open('tmpSpace/posLbToJpsiLam0.root')
canv=TCanvas('c1','c1',1600,1200)
canv.SaveAs(pdfFile+'[')
canv.SetFillColor(4000)
canv.SetFillStyle(4000)
mySavingROOTFilt=TFile('store_root/outHist_pLbL0_cuts.root', 'recreate')

plbl0=rootFile.Get('VertexCompCandAnalyzer/pLbL0')
nlbl0=rootFile.Get('VertexCompCandAnalyzer/nLbL0')
plbtk=rootFile.Get('VertexCompCandAnalyzer/pLbTk')
nlbtk=rootFile.Get('VertexCompCandAnalyzer/nLbTk')

muCutList=[ 4.0 ]
mumuCutList=[ -1., 16.0 ]
#ptkCutList=[ 1.0, 1.5, 2.0 ]
ptkCutList=[ -1.0 ]
#ntkCutList=[ 0.5, 1.0, 1.5 ]
ntkCutList=[ -1.0 ]
tktkCutList=[ 1.3, 1.5, 1.8 ]

cutMU='pmuPt>{0:.3f}&&nmuPt>{0:.3f}'
cutMUMU='(pmuP1+pmuP2)*(pmuP1+pmuP2)>{0:.3f}*{0:.3f}'
cutPTK='tk1Pt>{0:.3f}'
cutNTK='tk2Pt>{0:.3f}'
cutTKTK='tktkPt>{0:.3f}'
cutMassRange='lbtkMass>5.4&&lbtkMass<5.8'

for muCut in muCutList:
    for mumuCut in mumuCutList:
        for ptkCut in ptkCutList:
            for ntkCut in ntkCutList:
                for tktkCut in tktkCutList:
                    formatName='plbl0Mass'+'_mu{0:.3f}'.format(muCut)+'_mumu{0:.3f}'.format(mumuCut)+'_ptk{0:.3f}'.format(ptkCut)+'_ntk{0:.3f}'.format(ntkCut)+'_tktk{:.3f}'.format(tktkCut)
                    hisName=formatName.replace('-1.00','NO_').replace('.','')
                    myCutLists=[
                            cutMassRange,
                            cutMU.format(muCut),
                            cutMUMU.format(mumuCut),
                            cutPTK.format(ptkCut),
                            cutNTK.format(ntkCut),
                            cutTKTK.format(tktkCut)
                            ]


                    hist=TH1D(hisName, "",50,5.5,5.7)
                    plbl0.Draw('lbtkMass>>'+hisName, '&&'.join(myCutLists))
                    print 'hiiii --- {0}'.format(hist.GetEntries())
                    print 'hiiii --- '+'&&'.join(myCutLists)

                    hist.SetStats(False)
                    hist.SetTitle("#Lambda^{0}_{b}#rightarrow J/#psi p K under cut")
                    hist.GetXaxis().SetTitle('#Lambda^{0}_{b} Mass (GeV)')
                    hist.GetYaxis().SetTitle('event/4MeV')
                    hist.SetMaximum(hist.GetMaximum()*1.5)
                    hist.SetMinimum(0.)
                    hist.Draw()
                    hist.Write()

                    text=TPaveText(0.41,0.70,0.85,0.85,'NDC')
                    text.AddText('Total Entries {0}'.format(hist.GetEntries()))
                    text.SetFillStyle(4000)
                    text.SetFillColor(4000)
                    text.Draw('same')

                    canv.Modified()
                    canv.SaveAs('{}/h_{}.eps'.format(figFolder,hisName))
                    canv.SaveAs(pdfFile)

canv.SaveAs(pdfFile+']')
mySavingROOTFilt.Close()
rootFile.Close()
