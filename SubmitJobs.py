from glob import glob
import os,sys, optparse,argparse

test=False
path = sys.argv[2]

files =glob(path+'/*root')
fout = open('submit_condor-tmp2.sh','w')
#fin  = open('submit_condor-tmp.sh','r')
dataframefile = sys.argv[1]
#dataframefile='DataFrameToHisto_V1_R_hemRPBased.py'
#outputDir = sys.argv[3]
#if not os.path.isdir(outputDir):os.system('mkdir '+str(outputDir))

top='''#!/bin/sh
ulimit -s unlimited
set -e
cd /afs/cern.ch/user/d/dekumar/vertualInv 
python3 -m venv my_env
source my_env/bin/activate

'''
fout.write(top+'\n')
fout.write('\n')


for ii,ifile in enumerate(files):
	fout.write('if [ $1 -eq '+str(ii)+' ]; then'+'\n')
	fout.write('	python  '+dataframefile+'  -i   '+ifile+'\n')#'     -D   '+outputDir+'\n')
	fout.write('fi'+'\n')

fout.close()




top2='''executable = submit_condor-tmp2.sh
arguments = $(ProcId)
output                = output/condor.$(ClusterId).$(ProcId).out
error                 = error/condor.$(ClusterId).$(ProcId).err
log                   = log/condor.$(ClusterId).log

# Send the job to Held state on failure.
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

# Periodically retry the jobs every 10 minutes, up to a maximum of 5 retries.
periodic_release =  (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 600)

+JobFlavour="tomorrow"
'''

fout2=open('submit_condor-test.sub','w')

fout2.write(top2+'\n')
fout2.write('queue  '+str(len(files)))


if not test:os.system('condor_submit submit_condor-test.sub >& logjob.txt &')
