# with command lines under CMSSW_13_0_18: --mc --eventcontent RAWSIM --pileup HiMixGEN --datatier GEN-SIM --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM"  --nThreads 4 --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 4000

#------------------------------------
#GenXsecAnalyzer:
#------------------------------------
#Before Filter: total cross section = 1.819e+09 +- 1.090e+07 pb
#Filter efficiency (taking into account weights)= (8.4718) / (319.315) = 2.653e-02 +- 1.662e-03
#Filter efficiency (event-level)= (305) / (10000) = 3.050e-02 +- 1.720e-03    [TO BE USED IN MCM]

#After filter: final cross section = 4.827e+07 +- 3.038e+06 pb
#After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
#After filter: final equivalent lumi for 1M events (1/fb) = 2.072e-05 +- 1.304e-06
#TimeReport> Time report complete in 196.75 seconds 8 thread

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

            'CharmoniumShower:c2ccbar(3S1)[3S1(1)]c  = off,on',
            'CharmoniumShower:g2ccbar(3S1)[3S1(1)]gg = off,on',
            'CharmoniumShower:g2ccbar(3S1)[3S1(8)]  = off,on',

            'OniaShower:alphaScale   = 1',
            'OniaShower:ldmeFac      = 1000',					    
            'ColourReconnection:mode = 0',

            '100443:onMode = off',            # ignore cross-section re-weighting (CSAMODE=6) since selecting wanted decay mode
            '100443:onIfAny = 13 -13',

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
    MaxRapidity = cms.untracked.double(3.0),
    MinRapidity = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(0.0),
    ParticleID = cms.untracked.int32(100443)
)

mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(1., 1.),
    MinP = cms.untracked.vdouble(2.0, 2.0),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumugenfilter)
