#!/usr/bin/env python2
# this code don't cut kinematics due to bug in EDAnalyzer.
# I forgot to store the kinematics variable.

from ROOT import TFile, TNtupleD, TH1D, TCanvas, TLorentzVector, TChain
import os
pionMass=0.13957018
kaonMass=0.493677
ptonMass=0.9382720813

#OUTPUT_FILENAME='result_flatNtuple__LbL0.root'
#OUTPUT_FILENAME='store_root/result_flatNtuple_LbL0_noPreSelection.root'
OUTPUT_FILENAME='store_root/result_flatNtuple_LbL0_preSelection_noKinematicCut.root'



from array import array
if __name__ == "__main__":
    ipFile=TFile.Open('mc_data_mergedTree__LbL0All.root')
    dirNames=['pLbL0','nLbL0']
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
            fillNames=['lbl0Mass','lbl0Pt','mumuMass','mumuPt','mumuEta','tktkMass','tktkPt','tktkEta']
            fillPars={
                'lbl0Mass': [ 320, 4.8, 8.0 ],
                'lbl0Pt': [ 2000, 0., 200. ],
                'mumuMass': [ 70, 2.8, 3.5 ],
                'mumuPt': [ 500, 0., 50. ],
                'mumuEta': [ 240, -3.0,3.0 ],
                'tktkMass': [ 280, 0.2, 3.0 ],
                'tktkPt': [ 500, 0., 50. ],
                'tktkEta': [ 240, -3.0,3.0 ],
                }

            ntuple=TNtupleD( treeName, 'flat ntuple for roofit', ':'.join(fillNames))
            print ' joint names ' + ':'.join(fillNames) + 'with size = {0}'.format(len(fillNames))

            hists = { fillName : TH1D(treeName+'_'+fillName, fillName, num[0], num[1], num[2]) for fillName, num in fillPars.iteritems() }
            for event in mytree:
                    nCand=event.candSize

                    for i in range(nCand):
                        pmup4=TLorentzVector(event.pmuP1[i], event.pmuP2[i], event.pmuP3[i], event.pmuP0[i])
                        nmup4=TLorentzVector(event.nmuP1[i], event.nmuP2[i], event.nmuP3[i], event.nmuP0[i])
                        mumup4=pmup4+nmup4

                        ####### selection region ##########
                        #if event.tktkMass[i]<.115-0.05 or event.tktkMass[i]>1.115+0.05:
                        #    continue
                        #if event.tktkFlightDistanceSig[i] < 10.: continue
                        ####### selection region end ######

                        RecVals=[
                                event.lbtkMass[i], event.lbtkPt[i],
                                mumup4.Mag(), mumup4.Pt(), mumup4.Eta(),
                                event.tktkMass[i], event.tktkPt[i], event.tktkEta[i],
                                ]

                        ntuple.Fill( array('d', RecVals) )


                        for idx, val in enumerate(RecVals):
                            hists[fillNames[idx]].Fill(val)


            for name,hist in hists.iteritems():
                hist.Write()
            ntuple.Write()
    newFile.Close()

    os.system('mv processing.root {0}'.format(OUTPUT_FILENAME))

