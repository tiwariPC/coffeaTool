import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import data_2017.SFFactory_2017 as sf17
from coffea.lookup_tools.dense_lookup import dense_lookup

'''
fname = "/eos/cms/store/group/phys_exotica/monoHiggs/monoHbb/nanoAODtest/7E4CA912-5A6D-B14D-9E2E-09ED1E3318C9.root"
events = NanoEventsFactory.from_root(
    fname,
    schemaclass=NanoAODSchema.v7,
    metadata={"dataset": "MET"},
).events()
'''
fname = "/eos/cms/store/group/phys_exotica/monoHiggs/monoHbb/nanoAODtest/TTToSem_2017.root"

events = NanoEventsFactory.from_root(
    fname,
    schemaclass=NanoAODSchema.v7,
    metadata={"dataset": "TT"}
).events()



'''
=========================
List sections for objects
=======================

'''

muon_cond= (events.Muon.looseId==True) & (events.Muon.pt>10) & (events.Muon.pfIsoId==2)
#1=PFIsoVeryLoose, 2=PFIsoLoose, 3=PFIsoMedium, 4=PFIsoTight, 5=PFIsoVeryTight, 6=PFIsoVeryVeryTight
ele_cond = (events.Electron.cutBased==2) & (events.Electron.pt>10)

pho_cond = (events.Photon.pt>10) & (events.Photon.cutBased==2)

ak4_cond = abs(events.Jet.eta<2.5) & (events.Jet.pt>30) & (events.Jet.isTight==True)
#Jet_btagDeepB : Float_t DeepCSV b+bb tag discriminator

mwp = 0.4506	
ak4_bjet =  (events.Jet.btagDeepB>0.4506) & ak4_cond
ak8_index = abs(events.FatJet.eta<2.5) & (events.FatJet.pt>200) & (events.FatJet.isTight==True)


'''
Update leptons
'''
events['updatedElectron']=events.Electron[ele_cond]
events['updatedMuon']=events.Muon[muon_cond]
events['updatedPhoton']=events.Photon[pho_cond]







'''
=============================================================
ADD NEW AK4 COLOUMN FOR NEW JET COLLECTIONS
============================================================
'''

events['updatedJet']=events.Jet[ak4_cond]

''''
=======================================
Filters events with atleast two jets 
=======================================
'''

events = events[ak.num(events.updatedJet)>=2]

'''
=================================
Add coloum for bjets
===================================
'''
events['bJet']=events.updatedJet[events.updatedJet.btagDeepB>mwp]

'''
====================================
Filter events where you have 2 b jets
==================================
'''

events = events[ak.num(events.bJet)==2]

'''
========================
Compute Higgs mass 
=======================
'''
#higgs = events.bJet[:,0]+events.bJet[:,1]

events['DiJet'] = events.bJet[:,0]+events.bJet[:,1]


'''
compute MET SF
'''
corr_sf = dense_lookup(np.array(sf17.R_metTrig_firstmethod),np.array(sf.R_metTrig_firstmethod_X_range) )


'''
compute bjet sf 
'''
from coffea.btag_tools import BTagScaleFactor
btag_sf= BTagScaleFactor("data/DeepCSV_102XSF_V1.btag.csv.gz", "medium")
center =  btag_sf.eval("central", events.bJet.hadronFlavour, abs(events.bJet.eta), events.bJet.pt)
up     =  btag_sf.eval("up", events.Jet.hadronFlavour, abs(events.Jet.eta), events.Jet.pt)
down   = btag_sf.eval("down", events.Jet.hadronFlavour, abs(events.Jet.eta), events.Jet.pt)
events['bJet','sf'] = center
events['bJet','sfup'] = up
events['bJet','sfdown'] = down


'''
ADD weight for event weight
'''

from coffea.analysis_tools import Weights

weights = Weights(len(events))
weights.add("btagSF",weight=center[:,0]*center[:,1],weightUp=up[:,0]*up[:,1],weightDown=down[:,0]*down[:,1])

weights.add("metSF",weight=corr_sf(events.MET.pt),weightUp=corr_sf(events.MET.pt))


