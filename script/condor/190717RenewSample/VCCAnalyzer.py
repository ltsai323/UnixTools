#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms

process = cms.Process("analyzer")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Handle different input options
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register('targetPID',-1,VarParsing.multiplicity.singleton,VarParsing.varType.int,"set PID")
options.register('mcChannel',-1,VarParsing.multiplicity.singleton,VarParsing.varType.int,"set MC channel")
options.parseArguments()
inputFiles=[]
if len(options.inputFiles)==1 and (".root" not in options.inputFiles[0]):
    flist = open(options.inputFiles[0])
    inputFiles = flist.readlines()
    flist.close()

    inputFiles = [ 'root://se01.grid.nchc.org.tw/{0}'.format(i) for i in inputFiles ]
else:
    inputFiles = [ 'root://se01.grid.nchc.org.tw/{0}'.format(i) for i in options.inputFiles ]

#from histProduce.histProduce.data_bphOrig_cfi import files
#from histProduce.histProduce.data_2016RunG_LbL0_cfi import files
#process.source = cms.Source("PoolSource",fileNames = files,
process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring(
    inputFiles
#'root://se01.grid.nchc.org.tw//cms/store/user/ltsai/crabtest/MC/BdToJpsiKPi_BMuonFilter_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/ANTI_BdToJpsiKpi_append1_vertexProducer/190624_035111/0000/vertexProducer_BdRemoved_1-1.root'
#'/store/user/ltsai/vertexProducer/20181228revision/Charmonium/2016RunC_vertexProducer/181228_101222/0000/vertexProducer_BdRemoved_9.root'
#'file:///home/ltsai/ReceivedFile/tmp/vertexProducer_BdRemoved_1-10.root'
),
        duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)
print '------debugs-------- {0}'.format( inputFiles )


from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_2016LegacyRepro_v3', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '94X_dataRun2_ReReco_EOY17_v1', '')

# only choose event with LambdaB (+-5122)
process.load('vertexProducer.MCMatchTools.myGenSelector_cfi')
#process.myGenSelector.targetPIDs = cms.vint32(-5122) # choose Lb bar
##process.myGenSelector.targetPIDs = cms.vint32(-511) # choose Bd particle
#process.myGenSelector.mcChannel = cms.int32(7) # Bd->Jpsi + K + pi
#process.myGenSelector.mcChannel = cms.int32(8) # Bd->Jpsi + Kstar1430
#process.myGenSelector.mcChannel = cms.int32(9) # Bd->Jpsi + Kstar892
#process.myGenSelector.targetPIDs = cms.vint32(531) # choose Bs particle
#process.myGenSelector.mcChannel = cms.int32(5) # Bs->Jpsi + phi
#process.myGenSelector.mcChannel = cms.int32(4) # Bs->Jpsi + K + K
if options.targetPID != -1 and options.mcChannel != -1:
    process.myGenSelector.targetPIDs = cms.vint32(options.targetPID)
    process.myGenSelector.mcChannel = cms.int32(options.mcChannel)

process.TFileService = cms.Service('TFileService',
  fileName = cms.string('tree_VCCAnalyzer_forTest.root'),
  closeFileFast = cms.untracked.bool(True)
)

process.VertexCompCandAnalyzer = cms.EDAnalyzer('VertexCompCandAnalyzer',
    pL0BCandsLabel = cms.string("fourTracksFromVCCProducer:pL0B:myVertexingProcedure"),
    nL0BCandsLabel = cms.string("fourTracksFromVCCProducer:nL0B:myVertexingProcedure"),
    LbL0CandsLabel = cms.string("fourTracksFromVCCProducer:LbL0:myVertexingProcedure"),
    LbLoCandsLabel = cms.string("fourTracksFromVCCProducer:LbLo:myVertexingProcedure"),
    HLTRecordLabel = cms.string("TriggerResults::HLT"),
      bsPointLabel = cms.string("offlineBeamSpot::RECO")
)


process.p = cms.Path(
#       process.myGenSelector
       process.VertexCompCandAnalyzer
)
