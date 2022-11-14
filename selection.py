from coffea.analysis_tools import PackedSelection

selection = PackedSelection()

selection.add("noElectron", ak.num(events.updatedElectron) == 0)
selection.add("noMuon", ak.num(events.updatedMuon) == 0)
selection.add("noPhoton", ak.num(events.updatedPhoton) == 0)
selection.add("metcut", events.MET.pt > 200)
selection.add("nJets", ak.num(events.updatedJet)>=2)
selection.add("twobJets", ak.num(events.bJet)==2)

selection.add("leadbJetPt50", ak.any(events.bJet.pt >= 50.0, axis=1))


