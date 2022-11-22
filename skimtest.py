import awkward as ak
from coffea.nanoevents import NanoEventsFactory,BaseSchema
import uproot
#from bbMETProcessor_editing import bbMETProcessor
from bbMETProcessor import bbMETProcessor
#fname = '/eos/cms/store/group/phys_exotica/monoHiggs/bbMET/skimmedFiles/TTToSemiLeptonic_full.root'

#fname1='/eos/cms/store/group/phys_exotica/monoHiggs/bbMET/skimmedFiles/TTToSemiLeptonic.root'
fname = '/eos/cms/store/group/phys_exotica/monoHiggs/bbMET/skimmedFiles/TTTest.root'
#fname='/eos/cms/store/group/phys_exotica/monoHiggs/bbMET/2018_skimmedFiles/MET_AB.root'#
#fname='/eos/cms/store/group/phys_exotica/monoHiggs/bbMET/2018_skimmedFiles/v12.09_NoJERdata/MET-Run2018D-PromptReco-v2_146.root'

isData=True
tag="test"
outputpath="."#"/eos/cms/store/group/phys_exotica/monoHiggs/bbMET/coffeaoutput/2017/"+tag


dataset="TT"
f=uproot.open(fname)
totalweightedevents=f["h_total_mcweight"].values()[1]
totalevents=f["h_total"].values()[1]
filename=fname.split('/')[-1]
print (totalweightedevents)
events = NanoEventsFactory.from_root(
    fname,
    schemaclass=BaseSchema,
    treepath="outTree",
    metadata={"dataset":dataset,"isData":isData,"outputpath":outputpath,"filename":filename,"totalweightevents":float(totalweightedevents),"totalevents":int(totalevents)}
).events()



#treename="Events"

p = bbMETProcessor()
out = p.process(events)
print (out)
