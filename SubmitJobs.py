from glob import glob
import os,sys, optparse,argparse

test=False
path = sys.argv[4]
tag=sys.argv[3]
year  = sys.argv[2]
files =glob(path+'/*root')
dataframefile = sys.argv[1]
#if not os.path.isdir(outputDir):os.system('mkdir '+str(outputDir))
print ("total qurgumet",len(sys.argv))

top='''#!/bin/sh
ulimit -s unlimited
set -e
cd /afs/cern.ch/user/d/dekumar/vertualInv 
python3 -m venv my_env
source my_env/bin/activate

'''
count=sys.argv[5]
fout = open('submit_condor-tmp'+count+'.sh','w')
fout.write(top+'\n')
fout.write('\n')


for ii,ifile in enumerate(files):
	fout.write('if [ $1 -eq '+str(ii)+' ]; then'+'\n')
	fout.write('	python  '+dataframefile+' -m   -y '+year+'  -tag '+tag+'  -i   '+ifile+'\n')#'     -D   '+outputDir+'\n')
	fout.write('fi'+'\n')

fout.close()



top_='executable = submit_condor-tmp'+count+'.sh'
top2='''arguments = $(ProcId)
output                = output/condor.$(ClusterId).$(ProcId).out
error                 = error/condor.$(ClusterId).$(ProcId).err
log                   = log/condor.$(ClusterId).log

# Send the job to Held state on failure.
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

# Periodically retry the jobs every 10 minutes, up to a maximum of 5 retries.
periodic_release =  (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 600)

+JobFlavour="tomorrow"
'''

filename = 'submit_condor-test'+count+'.sub'

fout2=open(filename,'w')
fout2.write(top_+'\n')
fout2.write(top2+'\n')
fout2.write('queue  '+str(len(files))+'\n')
fout2.close()

#if len(sys.argv)==6:
#    os.system('cat submit_condor-tmp2.sh > info/submit_condor-tmp2'+sys.argv[5]+'.sh')
if not test:os.system('condor_submit '+filename)
# >& logjob.txt &')
