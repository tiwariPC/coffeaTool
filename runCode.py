import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import data_2017.SFFactory_2017 as sf17
from coffea.lookup_tools.dense_lookup import dense_lookup
from bbMETProcessor import myProcessor

fname = "/eos/cms/store/group/phys_exotica/monoHiggs/bbMET/nanoAODtest/TTToSem_2017.root"

events = NanoEventsFactory.from_root(
    fname,
    schemaclass=NanoAODSchema.v7,
    metadata={"dataset": "TT"}
).events()

p = myProcessor()
out = p.process(events)
print (out)
