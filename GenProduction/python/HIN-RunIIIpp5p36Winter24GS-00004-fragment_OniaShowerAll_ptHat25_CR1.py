# with command lines under CMSSW_13_0_18: --mc --eventcontent RAWSIM --pileup HiMixGEN --datatier GEN-SIM --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM"  --nThreads 4 --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 4000

# ------------------------------------
# GenXsecAnalyzer:
# ------------------------------------
# Before Filter: total cross section = 8.909e+06 +- 6.971e+04 pb
# Filter efficiency (taking into account weights)= (109.295) / (714.287) = 1.530e-01 +- 6.124e-03
# Filter efficiency (event-level)= (836) / (4000) = 2.090e-01 +- 6.429e-03    [TO BE USED IN MCM]

# After filter: final cross section = 1.363e+06 +- 5.559e+04 pb
# After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
# After filter: final equivalent lumi for 1M events (1/fb) = 7.336e-04 +- 2.993e-05

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
            #Pwave
            'CharmoniumShower:c2ccbar(3PJ)[3PJ(1)]c={on,on,on}',
            'CharmoniumShower:c2ccbar(3PJ)[3S1(8)]c={on,on,on}',
            'CharmoniumShower:g2ccbar(3PJ)[3PJ(1)]g={on,on,on}',
            'CharmoniumShower:g2ccbar(3PJ)[3S1(8)]={on,on,on}',
            #Swave, Singlet & Octet								
            'CharmoniumShower:c2ccbar(3S1)[3S1(1)]c={on,on}',
            'CharmoniumShower:g2ccbar(3S1)[3S1(1)]gg={on,on}',
            'CharmoniumShower:g2ccbar(3S1)[3S1(8)]={on,on}',

            'OniaShower:alphaScale = 1',
            'OniaShower:ldmeFac = 10000',					    
            '443:onMode = off',
            '443:onIfAny = 13 -13', # dimuon decay
            'PhaseSpace:pTHatMin = 25.',

            '443:onMode = off',            # ignore cross-section re-weighting (CSAMODE=6) since selecting wanted decay mode
            '443:onIfAny = 13 -13',
            #'PhaseSpace:pTHatMin = 2.',
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
