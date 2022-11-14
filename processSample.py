import awkward as ak
from coffea.nanoevents import NanoEventsFactory,BaseSchema
import uproot
from monoHbbProcessor import monoHbbProcessor
import sys, optparse,argparse
import os

usage = "python DataframeToHist.py -F -inDir directoryName -D outputDir "
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-i", "--inputfile",  dest="inputfile",default="myfiles.root")
parser.add_argument("-F", "--farmout", action="store_true",  dest="farmout")
parser.add_argument("-D", "--outputdir", dest="outputdir",default=".")
args = parser.parse_args()

infile  = args.inputfile

test=False
if not test:
    if '.root' in infile.split('/')[-1]:fname=infile
    if '.txt' in infile.split('/')[-1]:
        fname=open(infile).readline().rstrip()
else:
    fname='/eos/cms/store/group/phys_exotica/monoHiggs/monoHbb/skimmedFiles/TTToSemiLeptonic_full.root'
    #fname='/eos/cms/store/group/phys_exotica/monoHiggs/monoHbb/2018_skimmedFiles/v12.09_NoJERdata/MET-Run2018D-PromptReco-v2_146.root'


if 'Run' in fname.split('/')[-1] or 'MET' in fname.split('/')[-1]: isData = True
else:isData=False

if 'TTT' in fname.split('/')[-1]:dataset="TT"
else:dataset="other"

tag="V1_mcweight"
outputpath="/eos/cms/store/group/phys_exotica/monoHiggs/monoHbb/coffeaoutput/2017/"+tag
if not os.path.isdir(outputpath):os.system('mkdir -p '+outputpath)

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

p = monoHbbProcessor() 
out = p.process(events)
print (out)

