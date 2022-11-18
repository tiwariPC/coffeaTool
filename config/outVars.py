import awkward as ak
def fillbranch_R(events,goodevent,weights):
    events = events[goodevent]
    doc = {"DiJetMass":events.DiJetMass[:,0],"DiJetPt":events.DiJetPt[:,0],
           "bJet1Pt":events.bjetpt[:,0],
           "bJet2Pt":events.bjetpt[:,1],
           "MET":events.st_METXYCorr_Met,
           "CaloMET":events.st_pfpatCaloMETPt,
           #"fjetpt":ak.to_numpy(events.fjetpt),
           #"fjeteta":events.fjeteta,
           #"fjetphi":events.fjetphi,
           #"fjetmass":ak.to_numpy(events.fjetmass),
           #"fjetcsv":events.fjetcsv,
           "eventId":events.st_eventId,
           "minDphi":ak.to_numpy(events.minDphi_jetMet),
           "DPhi_trkpfMET":events.Dphi_trkpfMet,
           "weight":weights.weight()[goodevent]
          }
    return doc
         


def fillbranch_B(events,goodevent,weights):
    events = events[goodevent]
    doc = {"fjetpt":events.fjetpt[:,0],
           "fjeteta":events.fjeteta[:,0],
           "fjetphi":events.fjetphi[:,0],
           "fjetmass":events.fjetmass[:,0],
           "fjetcsv":events.fjetcsv[:,0],
           "MET":events.st_METXYCorr_Met,
           "CaloMET":events.st_pfpatCaloMETPt,
           "eventId":events.st_eventId,
           "minDphi":ak.to_numpy(events.minDphi_jetMet),
           "DPhi_trkpfMET":events.Dphi_trkpfMet,
           "weight":weights.weight()[goodevent]
          }
    return doc
