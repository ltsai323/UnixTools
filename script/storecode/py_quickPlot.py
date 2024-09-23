#!/usr/bin/env python2

from ROOT import TFile, TNtuple, TH1D, TCanvas, TLorentzVector, TChain
nbins=200
pdfName='checkcheck'

epsName='h_'

finalpdfName=pdfName+'.pdf'
useHLTpreselect=True
HLTNumber=7 # hire HLT_Dimuon20_Jpsi for 2016 Data
def passHLT(recIntBool, hltnum):
    if (recIntBool>>hltnum)%2 == 0: return False
    return True

def failMyPreselection(tree, candIdx ):
    if useHLTpreselect:
        if not passHLT( tree.totallyTriggered[candIdx], HLTNumber ): return True
    tk1p4=TLorentzVector(tree.tk1P1[candIdx], tree.tk1P2[candIdx], tree.tk1P3[candIdx], tree.tk1P0[candIdx])
    tk2p4=TLorentzVector(tree.tk2P1[candIdx], tree.tk2P2[candIdx], tree.tk2P3[candIdx], tree.tk2P0[candIdx])
    pmup4=TLorentzVector(tree.pmuP1[candIdx], tree.pmuP2[candIdx], tree.pmuP3[candIdx], tree.pmuP0[candIdx])
    nmup4=TLorentzVector(tree.nmuP1[candIdx], tree.nmuP2[candIdx], tree.nmuP3[candIdx], tree.nmuP0[candIdx])
    if tk1p4.Eta() >  2.5: return True
    if tk1p4.Eta() < -2.5: return True
    if tk2p4.Eta() >  2.5: return True
    if tk2p4.Eta() < -2.5: return True
    if pmup4.Eta() >  2.5: return True
    if pmup4.Eta() < -2.5: return True
    if nmup4.Eta() >  2.5: return True
    if nmup4.Eta() < -2.5: return True

    if (pmup4+nmup4).Pt() < 20.: return True
    if (tk1p4+tk2p4).Pt() < 1.3: return True
    #if tk1p4.Pt() < 0.8: return False
    #if tk2p4.Pt() < 0.3: return False

    return False




from array import array
if __name__ == "__main__":
    chain=TChain('VertexCompCandAnalyzer/pLbTk')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treedata_2016Bv2.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treedata_2016C.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treedata_2016D.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treedata_2016E.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treedata_2016F.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treedata_2016G.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treedata_2016H.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_BdJPsiKpi.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_BdJPsiKstar1430.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_BdJPsiKstar892.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_BsJPsiKK.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_aBdJPsiKpi.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_aBdJPsiKstar1430.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_aBdJPsiKstar892.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_aBsJPsiF2K1525.root')
    #chain.Add('/home/ltsai/Data/CRABdata/finalResult/treemc_aBsJPsiKK.root')
    chain.Add('tree_VCCAnalyzer_forTest.root')

    strs=['lbMass', 'fakeBsMass', 'fakeBdMass']
    interstrs=['pkMass', 'fakeKKMass', 'fakeKpiMass']
    pMass=[0.938272, 0.493677, 0.493677]
    nMass=[0.493677, 0.493677, 0.139570]
    h=[]
    h.append( (TH1D(strs[0],strs[0],nbins, 4.0, 8.0),TH1D('antiParticle_'+strs[0],'antiParticle_'+strs[0],nbins, 4.0, 8.0),TH1D(interstrs[0],interstrs[0],nbins, 0.5, 3.5),TH1D('antiParticle_'+interstrs[0],'antiParticle_'+interstrs[0],nbins, 0.5,3.5)))
    h.append( (TH1D(strs[1],strs[1],nbins, 4.0, 8.0),TH1D('antiParticle_'+strs[1],'antiParticle_'+strs[1],nbins, 4.0, 8.0),TH1D(interstrs[1],interstrs[1],nbins, 0.5, 3.5),TH1D('antiParticle_'+interstrs[1],'antiParticle_'+interstrs[1],nbins, 0.5,3.5)))
    h.append( (TH1D(strs[2],strs[2],nbins, 4.0, 8.0),TH1D('antiParticle_'+strs[2],'antiParticle_'+strs[2],nbins, 4.0, 8.0),TH1D(interstrs[2],interstrs[2],nbins, 0.5, 3.5),TH1D('antiParticle_'+interstrs[2],'antiParticle_'+interstrs[2],nbins, 0.5,3.5)))

    for event in chain:
        nCand=event.candSize

        keepEvent=False
        keepEvent=True


        #for candIdx in range(nCand):
        #    #if event.lbtkMass[i] > 6.0: continue
        #    #if event.lbtkMass[i] < 5.0: continue
        #    if failMyPreselection(event, i): continue
        #    passTag[i]=1
        #    keepEvent=True
        if not keepEvent:
            continue

        if nCand > 1:
            continue
        for candIdx in range(nCand):
            tk1p4=TLorentzVector(event.tk1P1[candIdx], event.tk1P2[candIdx], event.tk1P3[candIdx], event.tk1P0[candIdx])
            tk2p4=TLorentzVector(event.tk2P1[candIdx], event.tk2P2[candIdx], event.tk2P3[candIdx], event.tk2P0[candIdx])
            pmup4=TLorentzVector(event.pmuP1[candIdx], event.pmuP2[candIdx], event.pmuP3[candIdx], event.pmuP0[candIdx])
            nmup4=TLorentzVector(event.nmuP1[candIdx], event.nmuP2[candIdx], event.nmuP3[candIdx], event.nmuP0[candIdx])
            for idx, name in enumerate(strs):
                if pMass[idx] < 0. and nMass[idx] < 0.:
                    tk1p4.SetE( (tk1p4.P()**2+pMass[idx]**2)**0.5 )
                    tk2p4.SetE( (tk2p4.P()**2+nMass[idx]**2)**0.5 )
                    interFakeComp=tk1p4+tk2p4
                    fakeCompCand=interFakeComp+pmup4+nmup4

                    h[idx][0].Fill(fakeCompCand.Mag())
                    h[idx][2].Fill(interFakeComp.Mag())

                    tk1p4.SetE( (tk1p4.P()**2+nMass[idx]**2)**0.5 )
                    tk2p4.SetE( (tk2p4.P()**2+pMass[idx]**2)**0.5 )

                    interFakeComp=tk1p4+tk2p4
                    fakeCompCand=interFakeComp+pmup4+nmup4
                    h[idx][1].Fill(fakeCompCand.Mag())
                    h[idx][3].Fill(interFakeComp.Mag())
                    continue

                tk1p4.SetE( (tk1p4.P()**2+pMass[idx]**2)**0.5 )
                tk2p4.SetE( (tk2p4.P()**2+nMass[idx]**2)**0.5 )
                interFakeComp=tk1p4+tk2p4
                fakeCompCand=interFakeComp+pmup4+nmup4

                if interFakeComp.Mag()<0.85 or interFakeComp.Mag()>0.95:
                    continue

                h[idx][0].Fill(fakeCompCand.Mag())
                h[idx][2].Fill(interFakeComp.Mag())

                tk1p4.SetE( (tk1p4.P()**2+nMass[idx]**2)**0.5 )
                tk2p4.SetE( (tk2p4.P()**2+pMass[idx]**2)**0.5 )
                interFakeComp=tk1p4+tk2p4
                fakeCompCand=interFakeComp+pmup4+nmup4
                h[idx][1].Fill(fakeCompCand.Mag())
                h[idx][3].Fill(interFakeComp.Mag())

    canv=TCanvas('c1','',1600,1000)
    canv.SaveAs(finalpdfName+'[')
    for idx, name in enumerate(strs):
        h[idx][0].Draw()
        canv.SaveAs(finalpdfName)
        h[idx][1].Draw()
        canv.SaveAs(finalpdfName)
        h[idx][2].Draw()
        canv.SaveAs(finalpdfName)
        h[idx][3].Draw()
        canv.SaveAs(finalpdfName)
        #canv.SaveAs(epsName+name+'.eps')
    canv.SaveAs(finalpdfName+']')


