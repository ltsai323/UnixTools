#!/usr/bin/env python2

from ROOT import TFile, TNtupleD, TH1D, TCanvas, TLorentzVector, TChain
import os
pionMass=0.13957018
kaonMass=0.493677
ptonMass=0.9382720813

OUTPUT_FILENAME='store_root/result_flatNtuple_LbTk_myTestingCut.root'
#OUTPUT_FILENAME='store_root/result_flatNtuple_LbTk_preSelection_withKinematicCut.root'



from array import array
if __name__ == "__main__":
    ipFile=TFile.Open('store_root/mc_data_mergedTree__LbTkAll.root')
    dirNames=['pLbTk','nLbTk']
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
            'LbLo',
            'BdToJpsiKstar892',
            'BdToJpsiKstar1432',
            'BdToJpsiKpi',
            'BsToJpsiKK',
            'BsToJpsiPhi',
            'BsToJpsiF',
            'LbL0'
            ]

    newFile=TFile('processing.root', 'recreate')
    for dirName in dirNames:
        newDir=newFile.mkdir(dirName)
        newDir.cd()
        for treeName in treeNames:
            mytree=ipFile.Get(dirName+'/'+treeName)
            if mytree == None:
                print '{}  : not found! '.format(treeName)
                continue
            else:
                print '{}  : found! '.format(treeName)

            #fillNames=['lbtkMass','lbtkPt','lbtkbarMass','mumuMass','mumuPt','tktkMass','tktkPt','bsMass','kkMass','bdMass','kpiMass','bdbarMass','kpibarMass']
            fillNames=['lbtkMass','lbtkPt','lbtkbarMass','mumuMass','mumuPt','tktkMass','tktkPt','bsMass','kkMass','bdMass','kpiMass','bdbarMass','kpibarMass','tk1Pt','tk2Pt']
            #fillNames=['lbl0Mass','lbl0Pt','mumuMass','mumuPt','mumuEta','tktkMass','tktkPt','tktkEta']
            fillPars={
                'lbtkMass': [ 320, 4.8, 8.0 ],
                'lbtkPt': [ 2000, 0., 200. ],
                'lbtkbarMass': [ 320, 4.8, 8.0 ],
                'mumuMass': [ 70, 2.8, 3.5 ],
                'mumuPt': [ 500, 0., 50. ],
                'tktkMass': [ 280, 0.2, 3.0 ],
                'tktkPt': [ 500, 0., 50. ],
                'bsMass': [ 320, 4.8, 8.0 ],
                'kkMass': [ 220, 0.8, 3.0 ],
                'bdMass': [ 320, 4.8, 8.0 ],
                'kpiMass': [ 190, 0.6, 2.5 ],
                'bdbarMass': [ 320, 4.8, 8.0],
                'kpibarMass': [ 190, 0.6, 2.5 ],
                'tk1Pt': [100,0.,80.],
                'tk2Pt': [100,0.,80.],
                }

            ntuple=TNtupleD( treeName, 'flat ntuple for roofit', ':'.join(fillNames))
            print ' joint names ' + ':'.join(fillNames) + 'with size = {0}'.format(len(fillNames))

            hists = { fillName : TH1D(treeName+'_'+fillName, fillName, num[0], num[1], num[2]) for fillName, num in fillPars.iteritems() }
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

                        # I'll try this cuts!
                        ############### selection region #####################
                        #@if event.lbtkFlightDistanceSig[i]<15.: continue
                        #@if event.tktkCosa2d[i]<0.9: continue
                        #@if event.lbtkCosa2d[i]<0.999: continue
                        #@if event.lbtkVtxprob[i]<0.2: continue
                        #if event.tk1Pt[i]<3.: continue    # tk1Pt set as a variable to be used in further cut
                        #if event.tk2Pt[i]<2.: continue    # tk1Pt set as a variable to be used in further cut
                        ############### selection region end #################

                        RecVals=[
                                lbtkp4.Mag(),lbtkp4.Pt(),
                                lbtkbarp4.Mag(),
                                mumup4.Mag(), mumup4.Pt(),
                                tktkp4.Mag(), tktkp4.Pt(),
                                bsp4.Mag(), phip4.Mag(),
                                bdp4.Mag(), kstarp4.Mag(),
                                bdbarp4.Mag(), kstarbarp4.Mag(),
                                event.tk1Pt[i],event.tk2Pt[i]]

                        ntuple.Fill( array('d', RecVals) )


                        for idx, val in enumerate(RecVals):
                            hists[fillNames[idx]].Fill(val)


            for name,hist in hists.iteritems():
                hist.Write()
            ntuple.Write()
    newFile.Close()

    os.system('mv processing.root {0}'.format(OUTPUT_FILENAME))
    print('your file {0} is created'.format(OUTPUT_FILENAME))

