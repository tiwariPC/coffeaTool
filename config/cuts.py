

regions_R = {"sr": {"trigger":True,"noElectron":True, "noMuon":True, "noPhoton":True,"noTau":True,"metcut":True,"nJets":True,"twobJets":True,"bmass":True,"minDphi":True},
             "qcd":{"trigger":True,"noElectron":True, "noMuon":True, "noPhoton":True,"noTau":True,"metcut":True,"nJets":True,"twobJets":True,"bmass":True,"invrtminDphi":True}}



regions_B = {"sr": {"trigger":True,"noElectron":True, "noMuon":True, "noPhoton":True,"noTau":True,"metcut250":True,"nIsojet":True,"noIsobjet":True,"nfjet":True,"minDphi":True},
            "qcd":{"trigger":True,"noElectron":True, "noMuon":True, "noPhoton":True,"noTau":True,"metcut250":True,"nIsojet":True,"noIsobjet":True,"nfjet":True,"invrtminDphi":True}}


cutflow_R = {"trigger":{"trigger"},"eleVeto":{"noElectron"},"muonVeo":{"noElectron","noMuon"},"TauVeto":{"noElectron","noMuon","noTau"},"phoVeto":{"noElectron","noMuon","noPhoton"},"metcut":{"noElectron","noMuon","noPhoton","metcut"},"nJets":{"noElectron","noMuon","noPhoton","metcut","nJets"},"bJets":{"noElectron","noMuon","noPhoton","metcut","nJets","twobJets"},"mass":{"noElectron","noMuon","noPhoton","metcut","nJets","twobJets","bmass"},"minDphi":{"noElectron","noMuon","noPhoton","metcut","nJets","twobJets","bmass","minDphi"}}


cutflow_B = {"trigger":{"trigger"},"eleVeto":{"noElectron"},"muonVeo":{"noElectron","noMuon"},"TauVeto":{"noElectron","noMuon","noTau"},"phoVeto":{"noElectron","noMuon","noPhoton"},"metcut":{"noElectron","noMuon","noPhoton","metcut250"},"nfjet":{"noElectron","noMuon","noPhoton","metcut250","nfjet"},"nIsojet":{"noElectron","noMuon","noPhoton","metcut250","nfjet","nIsojet"},"noIsobjet":{"noElectron","noMuon","noPhoton","metcut250","nfjet","nIsojet","noIsobjet"},"minDphi":{"noElectron","noMuon","noPhoton","metcut250","nfjet","nIsojet","noIsobjet","minDphi"}}
