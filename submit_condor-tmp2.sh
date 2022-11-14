#!/bin/sh
ulimit -s unlimited
set -e
cd /afs/cern.ch/user/d/dekumar/vertualInv 
python3 -m venv my_env
source my_env/bin/activate



if [ $1 -eq 0 ]; then
	python  processSample.py  -i   /eos/cms/store/group/phys_exotica/monoHiggs/monoHbb/skimmedFiles/OneFile/Z2JetsToNuNu_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8.root
fi
