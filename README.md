# coffeaTool (Reading data with coffea NanoEvents)
### for more information : https://coffeateam.github.io/coffea/installation.html
### Nano AOD Data tier : https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD
coffea setup for monohbb run2


## Setup virtual environment (lxplus)
login into lxplus. Make a directory and setup vertual invironment  
```
mkdir coffeaFramework
cd coffeaFramework
python3 -m venv my_env
source my_env/bin/activate
pip install coffea
```

## copy code 
```

git clone git@github.com:deepakcern/coffeaTool.git

cd coffeaTool
```
When you login into lxplus. Please make sure to setup environment first using command ``` . setup ```

## Run Code

```
python  processSample.py -m   -y YEAR  -tag outputfolderName  -i rootfilename
```

