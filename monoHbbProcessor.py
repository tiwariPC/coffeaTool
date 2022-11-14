import awkward as ak
from coffea import processor
from coffea.nanoevents.methods import candidate
import hist
from coffea.analysis_tools import PackedSelection
import numpy as np
from coffea.btag_tools import BTagScaleFactor
from coffea.analysis_tools import Weights
from coffea.lookup_tools.dense_lookup import dense_lookup
import data_2017.SFFactory_2017 as sf17
from config.functions import *
from config.outVars import *
from coffea.lookup_tools import extractor
import uproot
from config.cuts import *


class monoHbbProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    
    def addWeights(self,events):
        weights = {"Boosted":Weights(len(events)),"Resolved":Weights(len(events))}
        #weights = Weights(len(events))
        corr_met = dense_lookup(np.array(sf17.R_metTrig_firstmethod),np.array(sf17.R_metTrig_firstmethod_X_range) )
        corr_met_B = dense_lookup(np.array(sf17.B_metTrig_firstmethod),np.array(sf17.B_metTrig_firstmethod_X_range) )
        corr_pu  = dense_lookup(np.array(sf17.pileup2017histo),np.array(sf17.pileup2017histo_X_range))

        weights["Boosted"].add("metSF",weight=corr_met_B(events.st_METXYCorr_Met),weightUp=corr_met_B(events.st_METXYCorr_Met),weightDown=corr_met_B(events.st_METXYCorr_Met))
        weights["Boosted"].add("pileupSF",weight=corr_pu(events.st_pu_nTrueInt),weightUp=corr_pu(events.st_pu_nTrueInt),weightDown=corr_pu(events.st_pu_nTrueInt))
    

        weights["Resolved"].add("metSF",weight=corr_met(events.st_METXYCorr_Met),weightUp=corr_met(events.st_METXYCorr_Met),weightDown=corr_met(events.st_METXYCorr_Met))
        weights["Resolved"].add("pileupSF",weight=corr_pu(events.st_pu_nTrueInt),weightUp=corr_pu(events.st_pu_nTrueInt),weightDown=corr_pu(events.st_pu_nTrueInt))


        weights["Boosted"].add("l1prefire",weight=events.st_prefiringweight,weightUp=events.st_prefiringweightup,weightDown=events.st_prefiringweightdown)
        weights["Resolved"].add("l1prefire",weight=events.st_prefiringweight,weightUp=events.st_prefiringweightup,weightDown=events.st_prefiringweightdown)
        weights["Boosted"].add("mcweight",weight=events.mcweight)
        weights["Resolved"].add("mcweight",weight=events.mcweight)

        ext = extractor()
        ext.add_weight_sets(["btag_eff_mwp efficiency_btag_mwp data_2017/bTagEffs_2017.root"])
        ext.add_weight_sets(["ctag_eff_mwp efficiency_ctag_mwp data_2017/bTagEffs_2017.root"])
        ext.add_weight_sets(["lighttag_eff_mwp efficiency_lighttag_mwp data_2017/bTagEffs_2017.root"])

        ext.add_weight_sets(["btag_eff_lwp efficiency_btag_lwp data_2017/bTagEffs_2017.root"])
        ext.add_weight_sets(["ctag_eff_lwp efficiency_ctag_lwp data_2017/bTagEffs_2017.root"])
        ext.add_weight_sets(["lighttag_eff_lwp efficiency_lighttag_lwp data_2017/bTagEffs_2017.root"])

        ext.finalize()
        evaluator = ext.make_evaluator()


        '''
        COMPUTE B TAG WEGIHTS FOR RESOLVED CATEGORY [FOR TAG AND NON TAG]
        '''

        btagIndex  = events.st_THINjetDeepCSV>0.4941        
        nonbtagIndex = ~btagIndex

        btag_sf_evaluator = BTagScaleFactor("data_2017/DeepCSV_94XSF_V5_B_F.csv.gz", "medium")
        
        
        btagCal=getbTagWegiht(btag_sf_evaluator,evaluator,events.st_THINjetHadronFlavor,events.jeteta,events.jetpt,btagIndex,nonbtagIndex,wptype="medium")


        weights["Resolved"].add("btagSF",weight=btagCal["btagSF"],weightUp=btagCal["btagSFUp"],weightDown=btagCal["btagSFDown"])
        weights["Resolved"].add("fakebSF",weight=btagCal["fakebSF"],weightUp=btagCal["fakebSFUp"],weightDown=btagCal["fakebSFDown"])

        '''
        ================= Compute b tag weights for boosted category ====
        '''
        isobtag_sf_evaluator = BTagScaleFactor("data_2017/DeepCSV_94XSF_V5_B_F.csv.gz", "loose")
        isobtagIndex  = events.isojetDeepCSV>0.1522
        isononbtagIndex = ~isobtagIndex

        isobtagCal=getbTagWegiht(isobtag_sf_evaluator,evaluator,events.isojetHadronFlavor,events.isojeteta,events.isojetpt,isobtagIndex,isononbtagIndex,wptype="loose")        
        weights["Boosted"].add("btagSF",weight=isobtagCal["btagSF"],weightUp=isobtagCal["btagSFUp"],weightDown=isobtagCal["btagSFDown"])
        weights["Boosted"].add("fakebSF",weight=isobtagCal["fakebSF"],weightUp=isobtagCal["fakebSFUp"],weightDown=isobtagCal["fakebSFDown"])        

        if events.metadata['dataset']=="TT":
            weights["Boosted"].add("topPtRewieght",weight=getTopPtReWgt(events.st_genParPt))
            weights["Resolved"].add("topPtRewieght",weight=getTopPtReWgt(events.st_genParPt))
        else:
            weights["Boosted"].add("topPtRewieght",np.ones(len(events)))


        return weights


#    def isobJetweight():
        

  
    def updateJetColl(self,events):
            ak4jeteta           =   geteta(events.st_THINjetPx,events.st_THINjetPy,events.st_THINjetPz)
            ak4jeteta_index     =   np.abs(ak4jeteta)<2.5
            events['st_THINjetPx']        =   events.st_THINjetPx[ak4jeteta_index]
            events['st_THINjetPy']        =   events.st_THINjetPy[ak4jeteta_index]
            events['st_THINjetPz']        =   events.st_THINjetPz[ak4jeteta_index]
            events['st_THINjetEnergy']    =   events.st_THINjetEnergy[ak4jeteta_index]
            events['st_THINjetDeepCSV']   =   events.st_THINjetDeepCSV[ak4jeteta_index]
            events['st_THINjetHadronFlavor']= events.st_THINjetHadronFlavor[ak4jeteta_index]
            events['st_THINjetCorrUnc']   =   events.st_THINjetCorrUnc[ak4jeteta_index]
            events['st_THINbRegNNCorr']   =   events.st_THINbRegNNCorr[ak4jeteta_index]

            events['st_THINjetNHadEF']    =   events.st_THINjetNHadEF[ak4jeteta_index]
            events['st_THINjetCHadEF']    =   events.st_THINjetCHadEF[ak4jeteta_index]
            events['st_THINjetCEmEF']     =   events.st_THINjetCEmEF[ak4jeteta_index]
            return events

 
    def addMainColoumns(self,events):

        events['jetpt']     =getpt(events.st_THINjetPx,events.st_THINjetPy)
        events['jeteta']    =geteta(events.st_THINjetPx,events.st_THINjetPy,events.st_THINjetPz)
        events['jetphi']    =getphi(events.st_THINjetPx,events.st_THINjetPy)


        events["minDphi_jetMet"]= np.abs(ak.min(DeltaPhi(events.jetphi, events.st_METXYCorr_MetPhi), axis=-1))

        events['fjetpt']    =getpt(events.st_fjetPx,events.st_fjetPy)
        events['fjeteta']   =geteta(events.st_fjetPx,events.st_fjetPy,events.st_fjetPz)
        events['fjetphi']   =getphi(events.st_fjetPx,events.st_fjetPy)
        
        fjet_sel = (np.abs(events.fjeteta) <2.5) & (events.st_fjetSDMass>70) & (events.st_fjetSDMass < 150) & (events.st_fjetProbHbb > 0.86)
        events['nfjet'] = ak.num(events.fjetpt[fjet_sel])
        events['fjetpt']= events.fjetpt[fjet_sel]
        events['fjeteta']= events.fjeteta[fjet_sel]
        events['fjetphi']= events.fjetphi[fjet_sel]
        events['fjetmass'] =events.st_fjetSDMass[fjet_sel]

        MWP = 0.4941
        bjetCond            =(events.st_THINjetDeepCSV>MWP) 
        events['bjetpt']    =events.jetpt[bjetCond]
        events['bjeteta']   =events.jeteta[bjetCond]
        events['bjetphi']   =events.jetphi[bjetCond]
        events['bjetHadronFla'] = events.st_THINjetHadronFlavor[bjetCond]
        events['bjetE']       =events.st_THINjetEnergy[bjetCond]
        bmass = getMassPair(events.st_THINjetPx[bjetCond],events.st_THINjetPy[bjetCond],events.st_THINjetPz[bjetCond],events.st_THINjetEnergy[bjetCond])
        events['DiJetMass']     = bmass
        parivars = getPair_ptetaphi(events.st_THINjetPx[bjetCond],events.st_THINjetPy[bjetCond],events.st_THINjetPz[bjetCond],events.st_THINjetEnergy[bjetCond])
        events['DiJetPt'] = parivars["pt"]
        events['DiJetEta'] = parivars["eta"]
        events['DiJetPhi'] = parivars["phi"]


        LWP = 0.1522


        cleaned = isclean(events.jeteta,events.fjeteta,events.jetphi,events.fjetphi,cut_=0.8)
        events['isojetpt']      = events.jetpt[cleaned]
        events['isojeteta']     = events.jeteta[cleaned]
        events['isojetphi']     = events.jetphi[cleaned]
        events['isojetDeepCSV'] = events.st_THINjetDeepCSV[cleaned]
        events['isojetHadronFlavor'] =events.st_THINjetHadronFlavor[cleaned]

        bjetCondForBoosted      = events.isojetDeepCSV>LWP

        events['isobjetpt']     =events.isojetpt[bjetCondForBoosted]
        events['isobjeteta']    =events.isojeteta[bjetCondForBoosted]
        events['isobjetphi']    =events.isojetphi[bjetCondForBoosted]
        

        # events['isobjetpt']     = events.isojetpt[cleanediso]
        # events['isobjeteta']    = events.isojeteta[cleanediso]
        # events['isobjetphi']    = events.isojetphi[cleanediso]


        events['elept']         = getpt(events.st_elePx, events.st_elePy)	
        events['eleeta']        =geteta(events.st_elePx, events.st_elePy, events.st_elePz)
        events['elephi']        =getphi(events.st_elePx, events.st_elePy)

        events['nlooseEle']     = ak.num(events.elept[(events.st_eleIsPassLoose)])
        events['ntightEle']     = ak.num(events.elept[(events.st_eleIsPassTight) & (events.elept > 40)])

        events['mupt']          = getpt(events.st_muPx,events.st_muPy)	
        events['mueta']         = geteta(events.st_muPx,events.st_muPy,events.st_muPz)
        events['muphi']         = getphi(events.st_muPx,events.st_muPy)

        events['nlooseMu']      = ak.num(events.mupt)
        events['ntightMu']      = ak.num(events.mupt[(events.st_isTightMuon) & (events.mupt>30)])

        events['phopt']         = getpt(events.st_phoPx, events.st_phoPy)
        events['phophi']        = getphi(events.st_phoPx, events.st_phoPy)
        events['phoeta']        = geteta(events.st_phoPx, events.st_phoPy,events.st_phoPz)

        cleanedPho = (isclean(events.phoeta,events.jeteta,events.phophi,events.jetphi,cut_=0.4)) & (events.phopt>20)
        events['npho']          = ak.num(events.phopt[cleanedPho])

        events['werecoilPt']     = getrecoil1(events.st_elePx,events.st_elePy,events.st_pfMetCorrPt,events.st_pfMetCorrPhi) 
        events['wmurecoilPt']     = getrecoil1(events.st_muPx,events.st_muPy,events.st_pfMetCorrPt,events.st_pfMetCorrPhi) 

        ele1px      = ak.Array(getN(events.st_elePx,1))
        ele0px      = ak.Array(getN(events.st_elePx,0))

        ele1py      = ak.Array(getN(events.st_elePy,1))
        ele0py      = ak.Array(getN(events.st_elePy,0))

        mu1px      = ak.Array(getN(events.st_muPx,1))
        mu0px      = ak.Array(getN(events.st_muPx,0))

        mu1py      = ak.Array(getN(events.st_muPy,1))
        mu0py      = ak.Array(getN(events.st_muPy,0))

        events['zeerecoilPt'] = getrecoil1(ele1px+ele0px,ele1py+ele0py,events.st_pfMetCorrPt,events.st_pfMetCorrPhi)
        events['zmumurecoilPt'] = getrecoil1(mu1px+mu0px,mu1py+mu0py,events.st_pfMetCorrPt,events.st_pfMetCorrPhi)




        return events
 
    def process(self, events):
        print ("code is running now")
        dataset = events.metadata['dataset']
        events  = self.updateJetColl(events)
        events  = self.addMainColoumns(events)
#        events  = events[events.st_eventId==26755655]
        '''
        ========================
        SISNAL REGION SELECTIONS
        =======================
        '''
        selection = PackedSelection()

        selection.add("trigger", events.st_mettrigdecision)
        selection.add("noElectron", (events.nlooseEle == 0 ) & (events.st_mettrigdecision))
        selection.add("noMuon", events.nlooseMu == 0)
        selection.add("noTau", events.st_nTau_discBased_looseElelooseMuVeto == 0)
        selection.add("noPhoton", (events.npho == 0) & (events.st_nTau_discBased_looseElelooseMuVeto == 0))
        selection.add("metcut", (events.st_METXYCorr_Met > 200))# & events.st_mettrigdecision)
        selection.add("metcut250", events.st_METXYCorr_Met > 250)
        selection.add("nJets", ak.num(events.jetpt)<=4)
        selection.add("twobJets", (ak.num(events.bjetpt)==2) & ak.any(events.bjetpt >= 50.0, axis=1))

        selection.add("leadbJetPt50", ak.any(events.bjetpt >= 50.0, axis=1))
        selection.add("bmass", ak.any(events.DiJetMass < 150,axis=1) & ak.any(events.DiJetMass > 100,axis=1))
        selection.add("minDphi",events.minDphi_jetMet>0.4)
        selection.add("nfjet",events.nfjet==1)
        selection.add("noIsobjet",ak.num(events.isobjetpt)==0)
        selection.add("nIsojet",ak.num(events.isojetpt)<=2)

        regions = {"sr": {"noElectron":True, "noMuon":True, "noPhoton":True,"metcut":True,"nJets":True,"twobJets":True,"bmass":True,"minDphi":True}}

        #cutflow = {"trigger":{"trigger"},"eleVeto":{"noElectron"},"muonVeo":{"noElectron","noMuon"},"TauVeto":{"noElectron","noMuon","noTau"},"phoVeto":{"noElectron","noMuon","noPhoton"},"metcut":{"noElectron","noMuon","noPhoton","metcut"},"nJets":{"noElectron","noMuon","noPhoton","metcut","nJets"},"bJets":{"noElectron","noMuon","noPhoton","metcut","nJets","twobJets"},"mass":{"noElectron","noMuon","noPhoton","metcut","nJets","twobJets","bmass"},"minDphi":{"noElectron","noMuon","noPhoton","metcut","nJets","twobJets","bmass","minDphi"}}

     
        #cutflow_B = {"trigger":{"trigger"},"eleVeto":{"noElectron"},"muonVeo":{"noElectron","noMuon"},"TauVeto":{"noElectron","noMuon","noTau"},"phoVeto":{"noElectron","noMuon","noPhoton"},"metcut":{"noElectron","noMuon","noPhoton","metcut250"},"nfjet":{"noElectron","noMuon","noPhoton","metcut250","nfjet"},"nIsojet":{"noElectron","noMuon","noPhoton","metcut250","nfjet","nIsojet"},"noIsobjet":{"noElectron","noMuon","noPhoton","metcut250","nfjet","nIsojet","noIsobjet"},"minDphi":{"noElectron","noMuon","noPhoton","metcut250","nfjet","nIsojet","noIsobjet","minDphi"}}

        if not events.metadata['isData']:
            weights = self.addWeights(events)
        else:
            weights = {"Boosted":Weights(len(events)),"Resolved":Weights(len(events))} 


        '''
        ============ START FILLING TREE ===========
        '''
	
        fout = uproot.recreate(events.metadata['outputpath']+'/'+events.metadata['filename'])
        for region, cuts in regions_R.items():
            goodevent = (selection.require(**cuts)) & (~selection.require(**regions_B[region]))
         #   weights = self.addWeights(events)[goodevent]
            if region.startswith("sr"):
                fout["monoHbb_SR_resolved"] = fillbranch_R(events,goodevent,weights["Resolved"])

        for region, cuts in regions_B.items():
           goodevent = selection.require(**cuts)
           if region.startswith("sr"):
                fout["monoHbb_SR_boosted"] = fillbranch_B(events,goodevent,weights["Boosted"])

        totalevents      =events.metadata['totalevents']
        totalweightevents=events.metadata['totalweightevents']
        h_total_mcweight = (hist.Hist.new.Reg(2, 0, 2, name="h_total_mcweight", label="").Weight())
        h_total          = (hist.Hist.new.Reg(2, 0, 2, name="h_total", label="").Weight())
        h_total_mcweight.fill(1)
        h_total.fill(1)
        fout["h_total_mcweight"] = h_total_mcweight * totalweightevents
        fout["h_total"]          = h_total * totalevents
        fout.close()


        '''
        ============ CUTFLOW ===========
        '''

        for lebel, cut in cutflow_B.items():
             goodevent = selection.all(*(cut))
             nev       = np.sum(goodevent)
             print(f"Events passing  in boosted {lebel}: {nev}")

        for lebel, cut in cutflow_R.items():
             goodevent = (selection.all(*(cut))) & (~selection.require(**regions_B["sr"]))
             nev       = np.sum(goodevent)#weights.weight()[goodevent].sum()#goodevent.sum()
             print(f"Events passing  {lebel}: {nev}")
             

        return {
            dataset: {
                "entries": len(events),
                #"mass": masshist,
        
              }
              }

    def postprocess(self, accumulator):
        pass

