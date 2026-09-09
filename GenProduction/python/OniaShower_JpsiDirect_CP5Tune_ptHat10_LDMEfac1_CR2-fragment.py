# with command lines under CMSSW_13_0_18: --mc --eventcontent RAWSIM --pileup HiMixGEN --datatier GEN-SIM --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM"  --nThreads 4 --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 4000

# ------------------------------------
# GenXsecAnalyzer:
# ------------------------------------
# Before Filter: total cross section = 1.807e+09 +- 1.087e+07 pb
# Filter efficiency (taking into account weights)= (0.155597) / (320.087) = 4.861e-04 +- 2.418e-04
# Filter efficiency (event-level)= (5) / (10025) = 4.988e-04 +- 2.230e-04    [TO BE USED IN MCM]

# After filter: final cross section = 8.785e+05 +- 4.370e+05 pb
# After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
# After filter: final equivalent lumi for 1M events (1/fb) = 1.138e-03 +- 5.663e-04

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

_generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(5362.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            #'Charmonium:states(3S1) = 443', # filter on 443 and prevents other onium states decaying to 443, so we should turn the others off
            'HardQCD:all = on',
            'CharmoniumShower:states(3S1)    = 443,100443', # filter on 443 and prevents other onium states decaying to 443, so we should turn the others off
            'CharmoniumShower:O(3S1)[3S1(1)] = 1.16,0.76',
            'CharmoniumShower:O(3S1)[3S1(8)] = 0.0119,0.0050',

            'CharmoniumShower:c2ccbar(3S1)[3S1(1)]c  = on,off',
            'CharmoniumShower:g2ccbar(3S1)[3S1(1)]gg = on,off',
            'CharmoniumShower:g2ccbar(3S1)[3S1(8)]  = on,off',

            'OniaShower:alphaScale   = 1',
            'OniaShower:ldmeFac      = 1',					    
            'ColourReconnection:mode = 2',

            '443:onMode = off',            # ignore cross-section re-weighting (CSAMODE=6) since selecting wanted decay mode
            '443:onIfAny = 13 -13',

            'PhaseSpace:pTHatMin = 10.',
            'PhaseSpace:bias2Selection = on',
            'PhaseSpace:bias2SelectionPow = 1.3',
            'PhaseSpace:bias2SelectionRef = 1'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
        )
)

from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter

generator = ExternalGeneratorFilter(_generator)

oniafilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxEta = cms.untracked.double(10.0),
    MinEta = cms.untracked.double(-10.0),
    MinPt = cms.untracked.double(0.0),
    ParticleID = cms.untracked.int32(443)
)

mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(0.5, 0.5),
    MinP = cms.untracked.vdouble(2.5, 2.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumugenfilter)
