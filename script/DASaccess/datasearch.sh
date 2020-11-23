#!/usr/bin/env sh

#das_client --query="dataset=/MuOnia*/*2016*PromptReco*/*"
#das_client --query="file dataset=/MuOnia/*2016C*BPH*/* " --idx=0 --limit=20
#das_client --query="dataset dataset=/Charmonium/*2016C*BPH*/* " --idx=0 --limit=20
#das_client --query="file dataset=/Charmonium/*2016C*BPH*/* " --idx=0 --limit=300
#das_client --query="dataset dataset=/Charmonium/*2016C*BPH*/* " --idx=0 --limit=300
#das_client --query="dataset dataset=/Charmonium/*2016C*/* "
#das_client --query="dataset dataset=/Charmonium/Run2016C-*/AOD" 
#das_client --query="file dataset=/Charmonium/Run2016C-18Apr2017-v1/AOD"  --idx=3  --limit=2
#das_client --query="dataset dataset=/Charmonium/Run2016C-BPHSkim-23Sep2016-v1/USER" --idx=0 --limit=40
#das_client --query="dataset dataset=/Lambda*13TeV*/*/MINIAODSIM"
#das_client --query="file dataset=/LambdaBToLambdaMuMu_SoftQCDnonDTest_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"
#das_client --query="file dataset=/LambdaBToLambdaMuMu_SoftQCDnonDTest_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM"
#das_client --query="file dataset=/LambdaBToLambdaMuMu_SoftQCDnonDTest_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM"
#das_client --query='file dataset=/Charmonium/Run2016C-BPHSkim-18Apr2017-v1/USER' --idx=8 --limit=2
#das_client --query='dataset dataset=/Charmonium/Run2016D*BPHSkim*/*' 

#das_client --query='dataset dataset=/Charmonium/Run2016*BPHSkim*/USER'
#das_client --query='dataset dataset=/*ToKK*/*80X*/AODSIM'
#das_client --query='release dataset=/BsToJpsiPhiV2_BFilter_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext1-v1/AODSIM' #CMSSW_7_4_1_patch4
#das_client --query='file dataset=/BsToJpsiPhiV2_BFilter_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext1-v1/AODSIM' --limit=2 #CMSSW_7_4_1_patch4
#das_client --query='dataset dataset=/BdToJpsiKstarV2_BFilter_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext1-v1/AODSIM'  #CMSSW_7_4_1_patch4

#das_client --query='file dataset=/InclusiveBtoJpsitoMuMu_JpsiPt3_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISpring16DR80-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/AODSIM' --idx=2 --limit=2  # CMSSW_8_0_3_patch2
#das_client --query='file dataset=/Charmonium/Run2016B-BPHSkim-18Apr2017_ver1-v1/USER' # CMSSW_8_0_28 EDProducer for Lb
#das_client --query='file dataset=/Charmonium/Run2016G-BPHSkim-18Apr2017-v1/USER' # CMSSW_8_0_28 EDProducer for Lb
#das_client --query='file dataset=/Charmonium/Run2016G-07Aug17-v1/AOD' --idx=2 --limit=1 # CMSSW_8_0_28 EDProducer for Lb
#das_client --query='dataset dataset=/LambdaBToLambdaJpsi*/*/AODSIM' # CMSSW_8_0_28 EDProducer for Lb
#das_client --query='dataset dataset=/Charmonium/Run2016C*/AOD'   # CMSSW_8_0_28 EDProducer for Lb
#das_client --query='file dataset=/Charmonium/Run2016B-07Aug17_ver2-v1/AOD' --idx=2 --limit=5   # CMSSW_8_0_28 EDProducer for Lb

# used for pileup input in step2 MC.
#das_client --query="file dataset=/Neutrino_E-10_gun/RunIISpring15PrePremix-PU2016_80X_mcRun2_asymptotic_v14-v2/GEN-SIM-DIGI-RAW" --idx=0 --limit=140
#das_client --query='dataset dataset=/DY*/*/MINIAODSIM'
#das_client --query='file dataset=/LambdaBToLambdaJpsi_LambdaToPiPi_JpsiToMuMu_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISpring16DR80-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/AODSIM' --idx=2 --limit=1 # my own MC for LambdaB->JPsi Lambda0
#das_client --query='dataset dataset=/Charmonium/Run2016*-07Aug17-v1/AOD'


#das_client --query='dataset dataset=/Charmonium/Run2017*-17Nov2017*/AOD'
#das_client --query='dataset dataset=/Charmonium/Run2017*-17Nov2017*/AOD' 
#das_client --query='dataset dataset=/*/*ltsai*/* instance=/prod/phys03'
#das_client --query='dataset dataset=/Charmonium/Run2016*07Aug17*/AOD' # CMSSW_8_0_28 EDProducer for Lb
#das_client --query='file dataset=/Charmonium/Run2016B-07Aug17_ver1-v1/AOD' --limit=1
#das_client --query='file dataset=/BsToJpsiF2p1525_BMuonFilter_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM' --limit=1
#das_client --query='file dataset=/BsToJpsiPhi_BMuonFilter_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/AODSIM' --limit=5
#das_client --query='file dataset=/BdToJpsiKPi_BMuonFilter_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM' --limit=10
#das_client --query='file dataset=/Charmonium/Run2016H-07Aug17-v1/AOD' --limit=2

#das_client --query='file dataset=/LambdaBToLambdaJpsi_LambdaToPiPi_JpsiToMuMu_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISpring16DR80-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/AODSIM' --limit=50
#das_client --query='file dataset=/SinglePhoton/Run2016H-EXOMONOPOLE-07Aug17-v1/USER' --limit=5

#das_client --query='dataset dataset=/GJet_Pt-*_TuneCUETP8M1-Flat_13TeV_pythia8_20M/RunIISummer16MiniAODv3-PUMoriond17_*/MINIAODSIM' # pythia flat sample
#das_client --query='dataset dataset=/GJet_Pt-15To6000_TuneCUETP8M1-Flat_13TeV_pythia8_20M/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6*-v1/MINIAODSIM' # pythia flat sample 80X not used
#das_client --query='dataset dataset=/G1Jet_Pt*_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_*94X_mcRun2_asymptotic*/MINIAODSIM' # amc@NLO 94X
#das_client --query='dataset dataset=/G1Jet_Pt*_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6*-v1/MINIAODSIM' # amc@NLO 80X not used
#das_client --query='dataset dataset=/GJets_HT-*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_*94X_mcRun2_asymptotic_*/MINIAODSIM' #madgraph 94X
#das_client --query='dataset dataset=/GJets_HT-*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6*-v1/MINIAODSIM' #madgraph 80X not used
#das_client --query='dataset dataset=/QCD_Pt_*to*_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_*94X_mcRun2_asymptotic_v3*/MINIAODSIM' #background samples_94X
#das_client --query='dataset dataset=/QCD_Pt_*to*_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_*/MINIAODSIM' #background samples_80x not used
#das_client --query='dataset dataset=/QCD_Pt_*to*_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM' #background samples_80x not used

das_client --query='file dataset=/G1Jet_Pt-50To100_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM' --limit=1
#das_client --query='release dataset=/G1Jet_Pt-50To100_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM'
#das_client --query='dataset dataset=/RelVal*/*/MINIAODSIM'
#das_client --query='dataset dataset=/*/*RelVal*/MINIAOD*'
#das_client --query='dataset dataset=/*TenTau_15_500*/*/MINIAODSIM'
#das_client --query='file dataset=/RelValTenTau_15_500/CMSSW_11_1_0_pre8-111X_mcRun3_2021_realistic_v4_PU25nsPMX-v1/MINIAODSIM' --limit=3
#das_client --query='file dataset=/RelValTenTau_15_500/CMSSW_10_6_4_patch1-PU25ns_106X_upgrade2018_realistic_v9_HS_resub-v1/MINIAODSIM' --limit=3
#das_client --query='dataset dataset=/*Tau*/*/MINIAODSIM' > aalist_Tau1
#das_client --query='dataset dataset=/*tau*/*/MINIAODSIM' > aalist_tau1
#das_client --query='dataset dataset=/*/*Tau*/MINIAODSIM' > aalist_Tau2
#das_client --query='dataset dataset=/*/*tau*/MINIAODSIM' > aalist_tau2
#das_client --query='file dataset=/RelValTenTau_15_500/CMSSW_11_1_0_pre8-110X_mcRun4_realistic_v3_2026D49noPU-v1/MINIAODSIM' 
#das_client --query="file dataset=/RelValTenTau_15_500/CMSSW_11_1_0_pre8-110X_mcRun4_realistic_v3_2026D49noPU-v1/GEN-SIM-RECO" --limit=1
#das_client --query="release dataset=/RelValZTT_14TeV/CMSSW_11_1_0_pre8-110X_mcRun4_realistic_v3_2026D49noPU-v1/GEN-SIM-RECO"
#das_client --query="dataset dataset=/QstarToGJ*/*/*"
#das_client --query="file dataset=/RelValZTT_14TeV/CMSSW_11_2_0_pre8-112X_mcRun4_realistic_v3_2026D49noPU-v1/GEN-SIM-RECO" --limit=2
#das_client --query="file dataset=/" --limit=2
