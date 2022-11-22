

regions = {
         "sr1b": {"mettrigger":True, "noElectron":True, "noMuon":True, "noPhoton":True, "noTau":True, "metcut":True, "nJetsSR1":True, "leadJetpt":True, "onebJet":True, "minDphi":True, "dpfCaloSR":True},

         "sr2b": {"mettrigger":True, "noElectron":True, "noMuon":True, "noPhoton":True, "noTau":True, "metcut":True, "nJetsSR2":True, "leadJetpt":True, "twobJets":True, "minDphi":True, "dpfCaloSR":True},

         "zee2j": {"eletrigger":True, "twoElectron":True, "noMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsZ1":True, "leadJetpt":True, "minDphi":True, "zeMass":True, "dpfCaloZeeCR":True},

         "zee3j": {"eletrigger":True, "twoElectron":True, "noMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsZ2":True, "leadJetpt":True, "minDphi":True, "zeMass":True, "dpfCaloZeCR":True},

         "zmumu2j": {"mettrigger":True, "noElectron":True, "twoMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsZ1":True, "leadJetpt":True, "minDphi":True, "zmuMass":True, "dpfCaloZmuCR":True},

         "zmumu3j": {"mettrigger":True, "noElectron":True, "twoMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsZ2":True, "leadJetpt":True, "minDphi":True, "zmuMass":True, "dpfCaloZmuCR":True},

         "we1b": {"eletrigger":True, "oneElectron":True, "noMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsW":True, "leadJetpt":True, "onebJet":True, "minDphi":True, "weMass":True, "dpfCaloWeCR":True},

         "wmu1b": {"mettrigger":True, "noElectron":True, "oneMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsW":True, "leadJetpt":True, "onebJet":True, "minDphi":True, "wmuMass":True, "dpfCaloWmuCR":True},

         "tope2b": {"eletrigger":True, "oneElectron":True, "noMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsTop":True, "leadJetpt":True, "onebJet":True, "minDphi":True, "weMass":True, "dpfCaloWeCR":True},

         "topmu2b": {"mettrigger":True, "noElectron":True, "oneMuon":True, "noPhoton":True, "noTau":True, "recoilcut":True, "nJetsTop":True, "leadJetpt":True, "onebJet":True, "minDphi":True, "wmuMass":True, "dpfCaloWmuCR":True}
}




cutflow = ['sr1b':{"trigger":{"mettrigger"},
            "eleVeto":{"mettrigger", "noElectron"},
            "muonVeo":{"mettrigger", "noElectron", "noMuon"},
            "tauVeto":{"mettrigger","noElectron", "noMuon", "noTau"},
            "phoVeto":{"mettrigger","noElectron", "noMuon", "noPhoton"},
            "metcut":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut"},
            "nJets":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR1", "leadJetpt"},
            "bJets":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR1",  "leadJetpt", "onebJet"},
            "minDphi":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR1", "leadJetpt", "onebJet", "minDphi"},
            "dpfCaloSR":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR1", "leadJetpt", "onebJet", "minDphi", "dpfCaloSR"}
         },
         'sr2b':{"trigger":{"mettrigger"},
            "eleVeto":{"mettrigger", "noElectron"},
            "muonVeo":{"mettrigger", "noElectron", "noMuon"},
            "tauVeto":{"mettrigger","noElectron", "noMuon", "noTau"},
            "phoVeto":{"mettrigger","noElectron", "noMuon", "noPhoton"},
            "metcut":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut"},
            "nJets":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR2", "leadJetpt"},
            "bJets":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR2",  "leadJetpt", "twobJets"},
            "minDphi":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR2", "leadJetpt", "twobJets", "minDphi"},
            "dpfCaloSR":{"mettrigger","noElectron", "noMuon", "noPhoton", "metcut", "nJetsSR2", "leadJetpt", "twobJets", "minDphi", "dpfCaloSR"}
         },
      ]
