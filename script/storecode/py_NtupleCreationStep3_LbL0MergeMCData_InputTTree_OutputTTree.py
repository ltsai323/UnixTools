#!/usr/bin/env python2
# this file merge MC and data. which is the thrid step.
# further apply pre-selection and HLT selection
# first step: EDProducer, second step: EDAnalyzer, third step: ###thisFile.py###
OUTPUT_FILENAME='mc_data_mergedTree__LbL0.root'

from ROOT import TFile, TNtuple, TH1D, TCanvas, TLorentzVector, TChain
import os

useHLTpreselect=True
HLTNumber=7 # hire HLT_Dimuon20_Jpsi for 2016 Data
def passHLT(recIntBool, hltnum):
    if (recIntBool>>hltnum)%2 == 0: return False
    return True

def failMyHLT(tree,candIdx):
    if useHLTpreselect:
        if not passHLT( tree.totallyTriggered[candIdx], HLTNumber ): return True
    return False
def failMyPreselection(tree, candIdx ):
    #tk1p4=TLorentzVector(tree.tk1P1[candIdx], tree.tk1P2[candIdx], tree.tk1P3[candIdx], tree.tk1P0[candIdx])
    #tk2p4=TLorentzVector(tree.tk2P1[candIdx], tree.tk2P2[candIdx], tree.tk2P3[candIdx], tree.tk2P0[candIdx])
    pmup4=TLorentzVector(tree.pmuP1[candIdx], tree.pmuP2[candIdx], tree.pmuP3[candIdx], tree.pmuP0[candIdx])
    nmup4=TLorentzVector(tree.nmuP1[candIdx], tree.nmuP2[candIdx], tree.nmuP3[candIdx], tree.nmuP0[candIdx])
    #if tk1p4.Eta() >  2.5: return True
    #if tk1p4.Eta() < -2.5: return True
    #if tk2p4.Eta() >  2.5: return True
    #if tk2p4.Eta() < -2.5: return True
    if pmup4.Eta() >  2.5: return True
    if pmup4.Eta() < -2.5: return True
    if nmup4.Eta() >  2.5: return True
    if nmup4.Eta() < -2.5: return True

    #print tree.GetName() + "   ---   tktk pt = {0}".format(tree.tktkPt[candIdx])
    # use dimuon jpsi pt > 20.
    if (pmup4+nmup4).Pt() < 20.: return True
    if tree.tktkPt[candIdx] < 1.3: return True
    if tree.tktkEta[candIdx] > 2.5: return True
    if tree.tktkEta[candIdx] <-2.5: return True
    #if (tk1p4+tk2p4).Pt() < 1.3: return True

    return False

def loadData(name):
    chain=TChain('VertexCompCandAnalyzer/{0}'.format(name))
    chain.Add('/home/ltsai/Data/CRABdata/finalResult/CRABdata_2016RunBv2_190516ReRunForFinal_11_06_2019/tot.root')
    chain.Add('/home/ltsai/Data/CRABdata/finalResult/CRABdata_2016RunC__190516ReRunForFinal_11_06_2019/tot.root')
    chain.Add('/home/ltsai/Data/CRABdata/finalResult/CRABdata_2016RunD__190516ReRunForFinal_12_06_2019/tot.root')
    chain.Add('/home/ltsai/Data/CRABdata/finalResult/CRABdata_2016RunF__190516ReRunForFinal_12_06_2019/tot.root')
    chain.Add('/home/ltsai/Data/CRABdata/finalResult/CRABdata_2016RunG__190516ReRunForFinal_12_06_2019/tot.root')
    return chain



from array import array
if __name__ == "__main__":
    newFile=TFile('creating.root', 'recreate')
    controlCenter={ 'pLbL0': True, 'nLbL0': True, }


    for branchTag, record in controlCenter.iteritems():
        if not record:
            continue

        dir=newFile.mkdir(branchTag)
        dir.cd()
        chain=loadData(branchTag)
        dataTree=chain.CloneTree(0)
        dataTree.SetName('2016Data')

        for event in chain:
                nCand=event.candSize
                keepEvent=False

                for i in range(nCand):
                    if failMyHLT(event,i): continue
                    if failMyPreselection(event, i): continue
                    keepEvent=True
                if keepEvent:
                    dataTree.Fill()
        dataTree.Write()

        mcfiles={
                'AntiLbTk':             ["/home/ltsai/Data/mcStep3_LbToPcK_13TeV_withoutPileUp_19426/treeSum_nL0B.root"],
                'AntiBdToJpsiKstar892': ['/home/ltsai/Data/condor/totTree_dir_ANTI_BdToJpsiKstar892.root'],
                'AntiBdToJpsiKstar1432':['/home/ltsai/Data/condor/totTree_dir_ANTI_BdToJpsiKstar1430.root'],
                'AntiBdToJpsiKpi':      ['/home/ltsai/Data/condor/totTree_dir_ANTI_BdToJpsiKpi.root'],
                'AntiBsToJpsiKK':       ['/home/ltsai/Data/condor/totTree_dir_ANTI_BsToJpsiKK.root'],
                'AntiBsToJpsiPhi':      [],
                'AntiBsToJpsiF':        ['/home/ltsai/Data/condor/totTree_dir_ANTI_BsToJpsiF2K1525.root'],
                'LbLo':                 ['/home/ltsai/Data/CRABdata/finalResult/totTree_dir_negLbToJpsiLam0.root'],
                'LbTk':                 ["/home/ltsai/Data/mcStep3_LbToPcK_13TeV_withoutPileUp_19426/treeSum_pL0B.root"],
                'BdToJpsiKstar892':     ['/home/ltsai/Data/condor/totTree_dir_BdToJpsiKstar892.root'],
                'BdToJpsiKstar1432':    ['/home/ltsai/Data/condor/totTree_dir_BdToJpsiKstar1430.root'],
                'BdToJpsiKpi':          ['/home/ltsai/Data/condor/totTree_dir_BdToJpsiKpi.root'],
                'BsToJpsiKK':           ['/home/ltsai/Data/condor/totTree_dir_BsToJpsiKK.root'],
                'BsToJpsiPhi':          [],
                'BsToJpsiF':            ['/home/ltsai/Data/condor/totTree_dir_BsToJpsiF2K1525.root'],
                'LbL0':                 ['/home/ltsai/Data/CRABdata/finalResult/totTree_dir_posLbToJpsiLam0.root'],
                }
        for mcName, files in mcfiles.iteritems():
            chain=TChain('VertexCompCandAnalyzer/{0}'.format(branchTag))
            if len(files) == 0:
                print mcName + " is skipped"
                continue
            for mcfile in files:
                chain.Add(mcfile)
            mctree=chain.CloneTree(0)
            mctree.SetName(mcName)

            for event in chain:
                nCand=event.candSize
                keepEvent=False

                for i in range(nCand):
                    if failMyPreselection(event,i): continue
                    keepEvent=True
                if keepEvent:
                    mctree.Fill()
            mctree.Write()

    newFile.Close()
    os.system('mv creating.root {0}'.format(OUTPUT_FILENAME))
