#Benchmark with command line options in CMSSW_14_1_6: Configuration/GenProduction/python/Psi2StoMuMuPiPi_pTHatMin4_5p36TeV_Pythia8TuneCP5_cfi.py --python_filename PsiToMuMuPiPi_GEN.py --eventcontent RAWSIM --datatier GEN-SIM --fileout file:Jpsi_GEN.root --conditions 141X_mcRun3_2024_realistic_ppRef5TeV_v7 --beamspot Realistic25ns13p6TeVEarly2023Collision --step GEN,SIM --geometry DB:Extended --era Run3_2024_ppRef --mc

# ------------------------------------
# GenXsecAnalyzer:
# ------------------------------------
# Before Filter: total cross section = 8.986e+06 +- 1.431e+05 pb
# Filter efficiency (taking into account weights)= (27.3178) / (179.524) = 1.522e-01 +- 1.253e-02
# Filter efficiency (event-level)= (177) / (1000) = 1.770e-01 +- 1.207e-02    [TO BE USED IN MCM]

# After filter: final cross section = 1.367e+06 +- 1.147e+05 pb
# After filter: final fraction of events with negative weights = 0.000e+00 +- 0.000e+00
# After filter: final equivalent lumi for 1M events (1/fb) = 7.313e-04 +- 6.136e-05
# TimeReport> Time report complete in 83.876 seconds

# 3.79 sec/event, 332 kB/event

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
            'Charmonium:states(3S1) = 100443', # filter on 100443 and prevents other onium states decaying to 100443, so we should turn the others off
            'Charmonium:O(3S1)[3S1(1)] = 1.16',
            'Charmonium:O(3S1)[3S1(8)] = 0.0119',
            'Charmonium:O(3S1)[1S0(8)] = 0.01',
            'Charmonium:O(3S1)[3P0(8)] = 0.01',
            'Charmonium:gg2ccbar(3S1)[3S1(1)]g = on',
            'Charmonium:gg2ccbar(3S1)[3S1(8)]g = on',
            'Charmonium:qg2ccbar(3S1)[3S1(8)]q = on',
            'Charmonium:qqbar2ccbar(3S1)[3S1(8)]g = on',
            'Charmonium:gg2ccbar(3S1)[1S0(8)]g = on',
            'Charmonium:qg2ccbar(3S1)[1S0(8)]q = on',
            'Charmonium:qqbar2ccbar(3S1)[1S0(8)]g = on',
            'Charmonium:gg2ccbar(3S1)[3PJ(8)]g = on',
            'Charmonium:qg2ccbar(3S1)[3PJ(8)]q = on',
            'Charmonium:qqbar2ccbar(3S1)[3PJ(8)]g = on',
            'Charmonium:gg2ccbar(3S1)[3S1(1)]gm = on',
            '100443:onMode = off',            # ignore cross-section re-weighting (CSAMODE=6) since selecting wanted decay mode
            '100443:onIfAny = 443 211 -211',
            '443:onMode = off',
            '443:onIfMatch = 13 -13',
            'PhaseSpace:pTHatMin = 2.0',
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
