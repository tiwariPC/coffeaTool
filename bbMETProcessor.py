import awkward as ak
from coffea import processor
from coffea.nanoevents.methods import candidate
import hist
from coffea.analysis_tools import PackedSelection
import numpy as np
from coffea.btag_tools import BTagScaleFactor
from coffea.analysis_tools import Weights
from coffea.lookup_tools.dense_lookup import dense_lookup

import data_2016.SFFactory_2016 as sf16
import data_2016.SFFactorySystUp_2016 as sf16Up
import data_2016.SFFactorySystDown_2016 as sf16Down

import data_2017.SFFactory_2017 as sf17
import data_2017.SFFactorySystUp_2017 as sf17Up
import data_2017.SFFactorySystDown_2017 as sf17Down

import data_2018.SFFactory_2018 as sf18
import data_2018.SFFactorySystUp_2018 as sf18Up
import data_2018.SFFactorySystDown_2018 as sf18Down

from config.functions import *
from config.outVars import *
from coffea.lookup_tools import extractor
import uproot
from config.cuts import *


class bbMETProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    def setupYearDependency(self,events):
        self.year = events.metadata["year"]
        if self.year=="2016":
            self.LWP = 0.2217
            self.MWP = 0.6321
            self.metSF = {"center":sf16.metTrig_firstmethod,"Up":sf16Up.metTrig_firstmethod_SystUp,"Down":sf16Down.metTrig_firstmethod_SystDown}
            self.metSFRange = sf16.metTrig_firstmethod_X_range
            self.PileReweightHisto  = {"center":sf16.pileup2016histo,"Up":sf16Up.pileup2016histo_SystUp,"Down":sf16Down.pileup2016histo_SystDown}
            self.PileReweightRange  = sf16.pileup2016histo_X_range
            self.btagEffroot   = "data_2016/bTagEffs_2016.root"
            self.btagCSVfile   = "data_2016/DeepCSV_2016LegacySF_V1.csv"

        if self.year=="2017":
            self.LWP = 0.1522
            self.MWP = 0.4941
            self.metSF = {"center":sf17.R_metTrig_firstmethod,"Up":sf17Up.R_metTrig_firstmethod_SystUp,"Down":sf17Down.R_metTrig_firstmethod_SystDown}
            self.metSFRange = sf17.R_metTrig_firstmethod_X_range
            self.PileReweightHisto  = {"center":sf17.pileup2017histo,"Up":sf17Up.pileup2017histo_SystUp,"Down":sf17Down.pileup2017histo_SystDown}
            self.PileReweightRange  = sf17.pileup2017histo_X_range
            self.btagEffroot   = "data_2017/bTagEffs_2017.root"
            self.btagCSVfile   = "data_2017/DeepCSV_94XSF_V5_B_F.csv"

        if self.year=="2018":
            self.LWP = 0.1241
            self.MWP = 0.4184
            self.metSF = {"center":sf18.R_metTrig_firstmethod,"Up":sf18Up.R_metTrig_firstmethod_SystUp,"Down":sf18Down.R_metTrig_firstmethod_SystDown}
            self.metSFRange = sf18.R_metTrig_firstmethod_X_range
            self.PileReweightHisto  = {"center":sf18.pileup2018histo,"Up":sf18Up.pileup2018histo_SystUp,"Down":sf18Down.pileup2018histo_SystDown}
            self.PileReweightRange  = sf18.pileup2018histo_X_range
            self.btagEffroot   = "data_2018/bTagEffs_2018.root"
            self.btagCSVfile   = "data_2018/DeepCSV_102XSF_V2.csv"


    def addWeights(self,events):
        weights  = Weights(len(events))
        corr_met = dense_lookup(np.array(self.metSF["center"]),np.array(self.metSFRange))
        corr_pu  = dense_lookup(np.array(self.PileReweightHisto["center"]),np.array(self.PileReweightRange))

        weights.add("metSF",weight=corr_met(events.st_pfMetCorrPt),weightUp=corr_met(events.st_pfMetCorrPt),weightDown=corr_met(events.st_pfMetCorrPt))
        weights.add("pileupSF",weight=corr_pu(events.st_pu_nTrueInt),weightUp=corr_pu(events.st_pu_nTrueInt),weightDown=corr_pu(events.st_pu_nTrueInt))
        weights.add("l1prefire",weight=events.st_prefiringweight,weightUp=events.st_prefiringweightup,weightDown=events.st_prefiringweightdown)
        weights.add("mcweight",weight=events.mcweight)

        ext = extractor()
        ext.add_weight_sets(["btag_eff_mwp efficiency_btag_mwp "+self.btagEffroot])
        ext.add_weight_sets(["ctag_eff_mwp efficiency_ctag_mwp "+self.btagEffroot])
        ext.add_weight_sets(["lighttag_eff_mwp efficiency_lighttag_mwp "+self.btagEffroot])

        ext.add_weight_sets(["btag_eff_lwp efficiency_btag_lwp "+self.btagEffroot])
        ext.add_weight_sets(["ctag_eff_lwp efficiency_ctag_lwp "+self.btagEffroot])
        ext.add_weight_sets(["lighttag_eff_lwp efficiency_lighttag_lwp "+self.btagEffroot])

        ext.finalize()
        evaluator = ext.make_evaluator()

        '''
        COMPUTE B TAG WEGIHTS FOR RESOLVED CATEGORY [FOR TAG AND NON TAG]
        '''
        MWP = self.MWP
        LWP = self.LWP
        btagIndex  = events.st_THINjetDeepCSV>MWP
        nonbtagIndex = ~btagIndex

        btag_sf_evaluator = BTagScaleFactor(self.btagCSVfile, "medium")

        btagCal=getbTagWegiht(btag_sf_evaluator,evaluator,events.st_THINjetHadronFlavor,events.jeteta,events.jetpt,btagIndex,nonbtagIndex,wptype="medium")

        weights.add("btagSF",weight=btagCal["btagSF"],weightUp=btagCal["btagSFUp"],weightDown=btagCal["btagSFDown"])
        weights.add("fakebSF",weight=btagCal["fakebSF"],weightUp=btagCal["fakebSFUp"],weightDown=btagCal["fakebSFDown"])

        # if events.metadata['dataset']=="TT":
        #     weights.add("topPtRewieght",weight=getTopPtReWgt(events.st_genParPt))
        # else:
        #     weights.add("topPtRewieght",weight=getTopPtReWgt(events.st_genParPt))

        return weights


    def updateJetColl(self,events):
        ak4jeteta                        =  geteta(events.st_THINjetPx,events.st_THINjetPy,events.st_THINjetPz)
        ak4jeteta_index                  =  np.abs(ak4jeteta)<2.5
        events['st_THINjetPx']           =  events.st_THINjetPx[ak4jeteta_index]
        events['st_THINjetPy']           =  events.st_THINjetPy[ak4jeteta_index]
        events['st_THINjetPz']           =  events.st_THINjetPz[ak4jeteta_index]
        events['st_THINjetEnergy']       =  events.st_THINjetEnergy[ak4jeteta_index]
        events['st_THINjetDeepCSV']      =  events.st_THINjetDeepCSV[ak4jeteta_index]
        events['st_THINjetHadronFlavor'] =  events.st_THINjetHadronFlavor[ak4jeteta_index]
        events['st_THINjetCorrUnc']      =  events.st_THINjetCorrUnc[ak4jeteta_index]
        events['st_THINbRegNNCorr']      =  events.st_THINbRegNNCorr[ak4jeteta_index]
        events['st_THINjetNHadEF']       =  events.st_THINjetNHadEF[ak4jeteta_index]
        events['st_THINjetCHadEF']       =  events.st_THINjetCHadEF[ak4jeteta_index]
        events['st_THINjetCEmEF']        =  events.st_THINjetCEmEF[ak4jeteta_index]
        return events


    def addMainColoumns(self,events):
        events['jetpt']  = getpt(events.st_THINjetPx,events.st_THINjetPy)
        events['jeteta'] = geteta(events.st_THINjetPx,events.st_THINjetPy,events.st_THINjetPz)
        events['jetphi'] = getphi(events.st_THINjetPx,events.st_THINjetPy)

        events["minDphi_jetMet"] = np.abs(ak.min(DeltaPhi(events.jetphi, events.st_pfMetCorrPhi), axis=-1))

        MWP = self.MWP
        bjetCond                = (events.st_THINjetDeepCSV>MWP)
        events['bjetpt']        = events.jetpt[bjetCond]
        events['bjeteta']       = events.jeteta[bjetCond]
        events['bjetphi']       = events.jetphi[bjetCond]
        events['bjetHadronFla'] = events.st_THINjetHadronFlavor[bjetCond]
        events['bjetE']         = events.st_THINjetEnergy[bjetCond]

        events['DiJetMass']     = getMassPair(events.st_THINjetPx[bjetCond],events.st_THINjetPy[bjetCond],events.st_THINjetPz[bjetCond],events.st_THINjetEnergy[bjetCond])
        parivars = getPair_ptetaphi(events.st_THINjetPx[bjetCond],events.st_THINjetPy[bjetCond],events.st_THINjetPz[bjetCond],events.st_THINjetEnergy[bjetCond])

        events['DiJetPt']  = parivars["pt"]
        events['DiJetEta'] = parivars["eta"]
        events['DiJetPhi'] = parivars["phi"]

        LWP = self.LWP#0.1522

        events['elept']  = getpt(events.st_elePx, events.st_elePy)
        events['eleeta'] = geteta(events.st_elePx, events.st_elePy, events.st_elePz)
        events['elephi'] = getphi(events.st_elePx, events.st_elePy)

        events['nlooseEle'] = ak.num(events.elept[(events.st_eleIsPassLoose)])
        events['ntightEle'] = ak.num(events.elept[(events.st_eleIsPassTight) & (events.elept > 35)])

        events['mupt']  = getpt(events.st_muPx,events.st_muPy)
        events['mueta'] = geteta(events.st_muPx,events.st_muPy,events.st_muPz)
        events['muphi'] = getphi(events.st_muPx,events.st_muPy)

        events['nlooseMu'] = ak.num(events.mupt)
        events['ntightMu'] = ak.num(events.mupt[(events.st_isTightMuon) & (events.mupt>30)])

        events['phopt']  = getpt(events.st_phoPx, events.st_phoPy)
        events['phophi'] = getphi(events.st_phoPx, events.st_phoPy)
        events['phoeta'] = geteta(events.st_phoPx, events.st_phoPy,events.st_phoPz)

        cleanedPho     = (isclean(events.phoeta,events.jeteta,events.phophi,events.jetphi,cut_=0.4)) & (events.phopt>20)
        events['npho'] = ak.num(events.phopt[cleanedPho])

        events['werecoilPt']    = getrecoil1(events.st_elePx,events.st_elePy,events.st_pfMetCorrPt,events.st_pfMetCorrPhi)
        events['wmurecoilPt']   = getrecoil1(events.st_muPx,events.st_muPy,events.st_pfMetCorrPt,events.st_pfMetCorrPhi)
        events['zeerecoilPt']   = getrecoil2(events.st_elePx,events.st_elePy,events.st_pfMetCorrPt,events.st_pfMetCorrPhi)
        events['zmumurecoilPt'] = getrecoil2(events.st_muPx,events.st_muPy,events.st_pfMetCorrPt,events.st_pfMetCorrPhi)

        events['delta_pfCaloSR'] = (events.st_pfpatCaloMETPt-events.st_pfMetCorrPt)/events.st_pfMetCorrPt

        events['delta_pfCaloZeeCR'] = (events.st_pfpatCaloMETPt-events.st_pfMetCorrPt)/events.zeerecoilPt
        events['delta_pfCaloZmumuCR'] = (events.st_pfpatCaloMETPt-events.st_pfMetCorrPt)/events.zmumurecoilPt
        events['delta_pfCaloWeCR'] = (events.st_pfpatCaloMETPt-events.st_pfMetCorrPt)/events.werecoilPt
        events['delta_pfCaloWmuCR'] = (events.st_pfpatCaloMETPt-events.st_pfMetCorrPt)/events.wmurecoilPt



        return events

    def process(self, events):
        print ('\n'+"================ Processor  is running now =================="+'\n')

        dataset = events.metadata['dataset']
        #events = events[(events.st_runId==306154) & (events.st_lumiSection==676) & (events.st_eventId==1161700016)]
        self.setupYearDependency(events)
        events  = self.updateJetColl(events)
        events  = self.addMainColoumns(events)
        '''
        ========================
        SIGNAL REGION SELECTIONS
        =======================
        '''
        selection = PackedSelection()

        selection.add("mettrigger",   events.st_mettrigdecision)
        selection.add("eletrigger",   events.st_eletrigdecision)
        selection.add("noElectron",   events.nlooseEle == 0 )
        selection.add("noMuon",       events.nlooseMu == 0)
        selection.add("noTau",        events.st_nTau_discBased_looseElelooseMuVeto == 0)
        selection.add("noPhoton",     events.npho == 0)
        selection.add("metcut",       events.st_pfMetCorrPt > 250)
        selection.add("nJetsSR1",     ak.num(events.jetpt)>=1 & ak.num(events.jetpt)<=2)
        selection.add("nJetsSR2",     ak.num(events.jetpt)>=2 & ak.num(events.jetpt)<=3)
        selection.add("nJetsZ1",      ak.num(events.jetpt)>=1 & ak.num(events.jetpt)<=2)
        selection.add("nJetsZ2",      ak.num(events.jetpt)>=2 & ak.num(events.jetpt)<=3)
        selection.add("nJetsW",       ak.num(events.jetpt)==1)
        selection.add("nJetsTop",     ak.num(events.jetpt)>1)
        selection.add("leadJetpt",    ak.any(events.jetpt >= 100.0, axis=1))
        selection.add("onebJet",      ak.num(events.bjetpt)==1)
        selection.add("twobJets",     ak.num(events.bjetpt)==2)
        selection.add("minDphi",      events.minDphi_jetMet>0.5)
        selection.add("oneElectron",  events.ntightEle==1)
        selection.add("oneMuon",      events.ntightMu==1)
        selection.add("twoElectron",  events.nlooseEle == 2 & (events.ntightEle==1 | events.ntightEle==2))
        selection.add("twoMuon",      events.nlooseMu == 2 & (events.ntightMu==1 | events.ntightMu==2))
        selection.add("dpfCaloSR",    events.delta_pfCaloSR < 0.5)
        selection.add("dpfCaloZeCR",  events.delta_pfCaloZeeCR < 0.5)
        selection.add("dpfCaloZmuCR", events.delta_pfCaloZmumuCR < 0.5)
        selection.add("dpfCaloWeCR",  events.delta_pfCaloWeCR < 0.5)
        selection.add("dpfCaloWmuCR", events.delta_pfCaloWmuCR < 0.5)
        selection.add("zeMass",       events.Zeemass >= 70 and events.Zeemass <= 110)
        selection.add("zmumass",      events.Zmumumass >= 70 and events.Zmumumass <= 110)
        selection.add("weMass",       events.Wenumass >= 0 and events.Wenumass <= 160)
        selection.add("wmuMass",      events.Wmunumass >= 0 and events.Wmunumass <= 160)
        selection.add("recoilcut",    ak.any(events.werecoilPt>250) | ak.any(events.wmurecoilPt>250) | ak.any(events.zmumurecoilPt>250) | ak.any(events.zeerecoilPt>250))

        '''
        --------------------------------------------
        GET EVENT WEIGHTS FOR MC AND SET 1 FOR DATA
        -------------------------------------------
        '''
        if not events.metadata['isData']:
            weights = self.addWeights(events)
        else:
            weights = {"Boosted":Weights(len(events)),"Resolved":Weights(len(events))}


        '''
        ============ START FILLING TREE ===========
        '''

        fout = uproot.recreate(events.metadata['outputpath']+'/'+events.metadata['filename'])

        for region, cuts in regions.items():
            goodevent = (selection.require(**cuts))
         #   weights = self.addWeights(events)[goodevent]
            fout["bbMET_"+region] = fillbranch(events,goodevent,weights)

        totalevents       = events.metadata['totalevents']
        totalweightevents = events.metadata['totalweightevents']
        h_total_mcweight  = (hist.Hist.new.Reg(2, 0, 2, name="h_total_mcweight", label="").Weight())
        h_total           = (hist.Hist.new.Reg(2, 0, 2, name="h_total", label="").Weight())
        h_total_mcweight.fill(1)
        h_total.fill(1)
        fout["h_total_mcweight"] = h_total_mcweight * totalweightevents
        fout["h_total"]          = h_total * totalevents



        '''
        ============ CUTFLOW ===========
        '''
        values = {"sr1b":[],"sr2b":[],"ze2j":[],"ze3j":[],"zmu2j":[],"zmu3j":[],"we1b":[],"wmu1b":[],"tope2b":[],"topmu2b":[]}
        for labels in cutflow:
            h_cutflow = (hist.Hist.new.Reg(int(len(labels)), 0, int(len(labels)), name="h_cutflow", label="").Weight())
            for label , cut in labels.items():
                goodevent = selection.all(*(cut))
                nev       = weights.weight()[goodevent].sum()
                values[label].append(nev)
                print(f"Events passing for : {label }: {nev}")
            fout["h_cutflow_"+label] = fillcutflow(h_cutflow,values[label])
        fout.close()

        return {
                dataset: {
                    "entries":totalweightevents, #len(events),
                    #"mass": masshist,
                    }
                }

    def postprocess(self, accumulator):
        pass
