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

class MyProcessor(processor.ProcessorABC):
    def __init__(self):
        pass

    
    def addWeights(self,events):
        weights = Weights(len(events))
        corr_met = dense_lookup(np.array(sf17.R_metTrig_firstmethod),np.array(sf17.R_metTrig_firstmethod_X_range) )
        corr_pu  = dense_lookup(np.array(sf17.pileup2017histo),np.array(sf17.pileup2017histo_X_range))

        weights.add("metSF",weight=corr_met(events.MET.pt),weightUp=corr_met(events.MET.pt),weightDown=corr_met(events.MET.pt))
        weights.add("pileupSF",weight=corr_pu(events.Pileup.nTrueInt),weightUp=corr_pu(events.Pileup.nTrueInt),weightDown=corr_pu(events.Pileup.nTrueInt))

        weights.add("l1prefire",weight=events.L1PreFiringWeight.Nom,weightUp=events.L1PreFiringWeight.Up,weightDown=events.L1PreFiringWeight.Dn)

        btag_sf_evaluator = BTagScaleFactor("data/DeepCSV_102XSF_V1.btag.csv.gz", "medium")
        btag_sf 	  =  btag_sf_evaluator.eval("central", events.bJet.hadronFlavour, abs(events.bJet.eta), events.bJet.pt)
        btag_sfUp 	  =  btag_sf_evaluator.eval("up", events.bJet.hadronFlavour, abs(events.bJet.eta), events.bJet.pt)
        btag_sfDown 	  =  btag_sf_evaluator.eval("down", events.bJet.hadronFlavour, abs(events.bJet.eta), events.bJet.pt)

        weights.add("btagSF",weight=ak.prod(btag_sf,axis=1),weightUp=ak.prod(btag_sfUp,axis=1),weightDown=ak.prod(btag_sfDown,axis=1))
        return weights
   
    def applypresel(self,events):
        muon_cond= (events.Muon.looseId==True) & (events.Muon.pt>10) & (events.Muon.pfIsoId==2)
        ele_cond = (events.Electron.cutBased==2) & (events.Electron.pt>10)
        pho_cond = (events.Photon.pt>10) & (events.Photon.cutBased==2)
        ak4_cond = abs(events.Jet.eta<2.5) & (events.Jet.pt>30) & (events.Jet.isTight==True)

        ak4_bjet =  (events.Jet.btagDeepB>0.4506) & ak4_cond


        events['updatedElectron']=events.Electron[ele_cond]
        events['updatedMuon']=events.Muon[muon_cond]
        events['updatedPhoton']=events.Photon[pho_cond]

        events['updatedJet']=events.Jet[ak4_cond]
#       mwp = 0.4506
        events['bJet']=events.updatedJet[events.updatedJet.btagDeepB>0.4506]
        return events
 
    def process(self, events):
        dataset = events.metadata['dataset']
        events  = self.applypresel(events)
        '''
        muon_cond= (events.Muon.looseId==True) & (events.Muon.pt>10) & (events.Muon.pfIsoId==2)
        ele_cond = (events.Electron.cutBased==2) & (events.Electron.pt>10)
        pho_cond = (events.Photon.pt>10) & (events.Photon.cutBased==2)
        ak4_cond = abs(events.Jet.eta<2.5) & (events.Jet.pt>30) & (events.Jet.isTight==True)

        ak4_bjet =  (events.Jet.btagDeepB>0.4506) & ak4_cond

	
        events['updatedElectron']=events.Electron[ele_cond]
        events['updatedMuon']=events.Muon[muon_cond]
        events['updatedPhoton']=events.Photon[pho_cond]

        events['updatedJet']=events.Jet[ak4_cond]
#	mwp = 0.4506
        events['bJet']=events.updatedJet[events.updatedJet.btagDeepB>0.4506]
        '''
        #
        '''
        ========================
        SISNAL REGION SELECTIONS
        =======================
        '''
        selection = PackedSelection()

        selection.add("noElectron", ak.num(events.updatedElectron) == 0)
        selection.add("noMuon", ak.num(events.updatedMuon) == 0)
        selection.add("noPhoton", ak.num(events.updatedPhoton) == 0)
        selection.add("metcut", events.MET.pt > 200)
        selection.add("nJets", ak.num(events.updatedJet)>=2)
        selection.add("twobJets", ak.num(events.bJet)==2)

        selection.add("leadbJetPt50", ak.any(events.bJet.pt >= 50.0, axis=1))

        regions = {"sr": {"noElectron":True, "noMuon":True, "noPhoton":True,"metcut":True,"nJets":True,"twobJets":True}}

        cutflow = {"eleVeto":{"noElectron"},"muonVeo":{"noElectron","noMuon"},"phoVeto":{"noElectron","noMuon","noPhoton"},"metcut":{"noElectron","noMuon","noPhoton","metcut"},"nJets":{"noElectron","noMuon","noPhoton","metcut","nJets"},"bJets":{"noElectron","noMuon","noPhoton","metcut","nJets","twobJets"}}

        weights = self.addWeights(events)
	
        masshist = (
    		hist.Hist.new
    		.StrCat(regions.keys(), name="region")
    		.StrCat(["nominal"], name="systematic")
    		.Reg(20, 0, 200, name="mass", label="$m_{bb}$ [GeV]")
    		.Weight()
		)

	

        for region, cuts in regions.items():
            goodevent = selection.require(**cuts)
         #   weights = self.addWeights(events)[goodevent]
            if region.startswith("sr"):
                mass = events.bJet[goodevent].sum().mass
                masshist.fill(
        		region=region,
        		systematic="nominal",
        		mass=mass,
        		weight=weights.weight()[goodevent],
        		)

        for lebel, cut in cutflow.items():
             goodevent = selection.all(*(cut))
             nev       = weights.weight()[goodevent].sum()#goodevent.sum()
             print(f"Events passing  {cut}: {nev}")
             

        return {
            dataset: {
                "entries": len(events),
                "mass": masshist,
        
              }
              }

    def postprocess(self, accumulator):
        pass

