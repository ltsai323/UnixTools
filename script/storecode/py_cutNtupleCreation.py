#!/usr/bin/env python2

from ROOT import TFile, TNtupleD, TH1D, TCanvas, TLorentzVector, TChain
pionMass=0.13957018
kaonMass=0.493677
ptonMass=0.9382720813



from array import array
if __name__ == "__main__":
    ipFile=TFile.Open('mc_data_mergedTree.root')
    treeNames=[
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

    newFile=TFile('data_treeForCUT.root', 'recreate')
    for treeName in treeNames:
        mytree=ipFile.Get(treeName)
        if mytree == None:
            print '{}  : not found! '.format(treeName)
            continue
        else:
            print '{}  : found! '.format(treeName)

        fillNames=[
                'lbtkMass','lbtkPt','lbtkbarMass',
                'lbtkCosa2d','lbtkVtxProb','lbtknChi2','lbtkFD2d','lbtkFDsig',
                'tktkMass','tktkPt',
                'tktkCosa2d','tktkVtxProb','tktknChi2','tktkFD2d','tktkFDsig',
                'tk1Pt','tk2Pt',
                'bsMass','kkMass','bdMass','kpiMass','bdbarMass','kpibarMass'
                ]

        ntuple=TNtupleD( treeName, 'flat ntuple for roofit', ':'.join(fillNames) )
        print ' joint names ' + ':'.join(fillNames) + 'with size = {0}'.format(len(fillNames))

        for event in mytree:
                nCand=event.candSize

                for i in range(nCand):
                    tk1p4=TLorentzVector(event.tk1P1[i], event.tk1P2[i], event.tk1P3[i], event.tk1P0[i])
                    tk2p4=TLorentzVector(event.tk2P1[i], event.tk2P2[i], event.tk2P3[i], event.tk2P0[i])
                    pmup4=TLorentzVector(event.pmuP1[i], event.pmuP2[i], event.pmuP3[i], event.pmuP0[i])
                    nmup4=TLorentzVector(event.nmuP1[i], event.nmuP2[i], event.nmuP3[i], event.nmuP0[i])
                    mumup4=pmup4+nmup4
                    tktkp4=tk1p4+tk2p4

                    tk1p4.SetE((ptonMass*ptonMass+tk1p4.P()*tk1p4.P())**0.5)
                    tk2p4.SetE((kaonMass*kaonMass+tk2p4.P()*tk2p4.P())**0.5)
                    lbtkp4=tk1p4+tk2p4+pmup4+nmup4
                    tktkp4=tk1p4+tk2p4

                    tk1p4.SetE((kaonMass*kaonMass+tk1p4.P()*tk1p4.P())**0.5)
                    tk2p4.SetE((ptonMass*ptonMass+tk2p4.P()*tk2p4.P())**0.5)
                    lbtkbarp4=tk1p4+tk2p4+pmup4+nmup4
                    tktkbarp4=tk1p4+tk2p4

                    tk1p4.SetE((kaonMass*kaonMass+tk1p4.P()*tk1p4.P())**0.5)
                    tk2p4.SetE((kaonMass*kaonMass+tk2p4.P()*tk2p4.P())**0.5)
                    bsp4=tk1p4+tk2p4+pmup4+nmup4
                    phip4=tk1p4+tk2p4

                    tk1p4.SetE((kaonMass*kaonMass+tk1p4.P()*tk1p4.P())**0.5)
                    tk2p4.SetE((pionMass*pionMass+tk2p4.P()*tk2p4.P())**0.5)
                    bdp4=tk1p4+tk2p4+pmup4+nmup4
                    kstarp4=tk1p4+tk2p4

                    tk1p4.SetE((pionMass*pionMass+tk1p4.P()*tk1p4.P())**0.5)
                    tk2p4.SetE((kaonMass*kaonMass+tk2p4.P()*tk2p4.P())**0.5)
                    bdbarp4=tk1p4+tk2p4+pmup4+nmup4
                    kstarbarp4=tk1p4+tk2p4

                    recVals=[
                            lbtkp4.Mag(),lbtkp4.Pt(), lbtkbarp4.Mag(),
                            event.lbtkCosa2d[i], event.lbtkVtxprob[i], event.lbtknChi2[i], event.lbtkFlightDistance2d[i], event.lbtkFlightDistanceSig[i],
                            tktkp4.Mag(), tktkp4.Pt(),
                            event.tktkCosa2d[i], event.tktkVtxprob[i], event.tktknChi2[i], event.tktkFlightDistance2d[i], event.tktkFlightDistanceSig[i],
                            tk1p4.Pt(), tk2p4.Pt(),
                            bsp4.Mag(), phip4.Mag(),
                            bdp4.Mag(), kstarp4.Mag(),
                            bdbarp4.Mag(), kstarbarp4.Mag()
                            ]
                    ntuple.Fill( array('d', recVals) )
        ntuple.Write()
    newFile.Close()


