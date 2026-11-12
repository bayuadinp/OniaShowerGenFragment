# with command lines under CMSSW_13_0_18: --mc --eventcontent RAWSIM --pileup HiMixGEN --datatier GEN-SIM --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM"  --nThreads 4 --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 4000

#------------------------------------
#GenXsecAnalyzer:
#------------------------------------
#Before Filter: total cross section = 2.656e+09 +- 1.613e+07 pb
#Filter efficiency (taking into account weights)= (8.62156) / (326.942) = 2.637e-02 +- 1.648e-03
#Filter efficiency (event-level)= (310) / (10000) = 3.100e-02 +- 1.733e-03    [TO BE USED IN MCM]

#After filter: final cross section = 7.003e+07 +- 4.396e+06 pb
#After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
#After filter: final equivalent lumi for 1M events (1/fb) = 1.428e-05 +- 8.965e-07
#TimeReport> Time report complete in 1025.71 seconds

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(5362.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP1SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:all = on',
            'CharmoniumShower:states(3S1)    = 443,100443', # filter on 100443 and prevents other onium states decaying to 100443, so we should turn the others off
            
            'CharmoniumShower:O(3S1)[3S1(1)] = 1.16,0.76',
            'CharmoniumShower:O(3S1)[3S1(8)] = 0.0119,0.0050',

            'CharmoniumShower:c2ccbar(3S1)[3S1(1)]c  = off,on',
            'CharmoniumShower:g2ccbar(3S1)[3S1(1)]gg = off,on',
            'CharmoniumShower:g2ccbar(3S1)[3S1(8)]  = off,on',

            'OniaShower:alphaScale   = 1',
            'OniaShower:ldmeFac      = 1000',					    
            'ColourReconnection:mode = 2',

            '100443:onMode = off',            # ignore cross-section re-weighting (CSAMODE=6) since selecting wanted decay mode
            '100443:onIfAny = 443 211 -211', # psi2s to jpsi +pipi
            '443:onMode = off',            
            '443:onIfAny = 13 -13',          # jpsi to mumu

            'PhaseSpace:pTHatMin = 10.',
            'PhaseSpace:bias2Selection = on',
            'PhaseSpace:bias2SelectionPow = 1.3',
            'PhaseSpace:bias2SelectionRef = 1'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP1Settings',
                                    'processParameters',
                                    )
        )
)

psi2SIDfilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(0.0),
    ParticleID = cms.untracked.int32(100443)
)

jpsiIDfilter = cms.EDFilter("PythiaFilter",
    ParticleID = cms.untracked.int32(443),
    MinPt = cms.untracked.double(0.0),
    MinEta = cms.untracked.double(-3.0),
    MaxEta = cms.untracked.double(3.0),
    Status = cms.untracked.int32(2)
)

mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(1., 1.),
    MinP = cms.untracked.vdouble(0.0, 0.0),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)
piminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.0),
    ParticleID = cms.untracked.int32(100443),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-3.0),
    MaxEta = cms.untracked.vdouble(3.0),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(-211)
)
piplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.0),
    ParticleID = cms.untracked.int32(100443),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.4),
    MaxEta = cms.untracked.vdouble(2.4),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(211)
)

ProductionFilterSequence = cms.Sequence(generator*psi2SIDfilter*jpsiIDfilter*mumugenfilter*piminusfilter*piplusfilter)
