# with command lines under CMSSW_13_0_18: --mc --eventcontent RAWSIM --pileup HiMixGEN --datatier GEN-SIM --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM"  --nThreads 4 --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 4000

# ------------------------------------
# GenXsecAnalyzer:
# ------------------------------------
# Before Filter: total cross section = 6.033e+07 +- 2.569e+06 pb
# Filter efficiency (taking into account weights)= (2.09146) / (2.4088) = 8.683e-01 +- 2.371e-02
# Filter efficiency (event-level)= (204) / (232) = 8.793e-01 +- 2.139e-02    [TO BE USED IN MCM]

# After filter: final cross section = 5.238e+07 +- 2.650e+06 pb
# After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
# After filter: final equivalent lumi for 1M events (1/fb) = 1.909e-05 +- 9.660e-07

# 0.27 sec/output event, 825 kB/output event

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
            #'Charmonium:O(3S1)[3S1(1)] = 1.16',
            #'Charmonium:O(3S1)[3S1(8)] = 0.0119',
            #'Charmonium:O(3S1)[1S0(8)] = 0.01',
            #'Charmonium:O(3S1)[3P0(8)] = 0.01',
            #'Charmonium:gg2ccbar(3S1)[3S1(1)]g = on',
            #'Charmonium:gg2ccbar(3S1)[3S1(8)]g = on',
            #'Charmonium:qg2ccbar(3S1)[3S1(8)]q = on',
            #'Charmonium:qqbar2ccbar(3S1)[3S1(8)]g = on',
            #'Charmonium:gg2ccbar(3S1)[1S0(8)]g = on',
            #'Charmonium:qg2ccbar(3S1)[1S0(8)]q = on',
            #'Charmonium:qqbar2ccbar(3S1)[1S0(8)]g = on',
            #'Charmonium:gg2ccbar(3S1)[3PJ(8)]g = on',
            #'Charmonium:qg2ccbar(3S1)[3PJ(8)]q = on',
            #'Charmonium:qqbar2ccbar(3S1)[3PJ(8)]g = on',
            #'Charmonium:gg2ccbar(3S1)[3S1(1)]gm = on',
            'HardQCD:all = on',
            'CharmoniumShower:all = off',
            # Octet								
            'CharmoniumShower:g2ccbar(3S1)[3S1(8)]= on,off',

            'OniaShower:alphaScale = 1',
            'OniaShower:ldmeFac = 10000',					   
            'ColourReconnection:mode = 1',
            'BeamRemnants:remnantMode = 1.',
            

            '443:onMode = off',            # ignore cross-section re-weighting (CSAMODE=6) since selecting wanted decay mode
            '443:onIfAny = 13 -13',
            'PhaseSpace:pTHatMin = 25.',
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
