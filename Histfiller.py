regions = {
    "sr": {"noElectron":True, "noMuon":True, "noPhoton":True,"metcut":True,"nJets":True,"twobJets":True},
 #   "eeSS": {"twoElectron": True, "noMuon": True, "leadPt20": True, "eleOppSign": False},
 #   "mm": {"twoMuon": True, "noElectron": True, "leadPt20": True, "muOppSign": True},
 #   "mmSS": {"twoMuon": True, "noElectron": True, "leadPt20": True, "muOppSign": False},
}

masshist = (
    hist.Hist.new
    .StrCat(regions.keys(), name="region")
    .StrCat(["nominal"] + list(weights.variations), name="systematic")
    .Reg(20, 0, 200, name="mass", label="$m_{bb}$ [GeV]")
    .Weight()
)

for region, cuts in regions.items():
    goodevent = selection.require(**cuts)
    if region.startswith("sr"):
        mass = events.bJet[goodevent].sum().mass
	masshist.fill(
        region=region,
        systematic="nominal",
        mass=mass,
        weight=weights.weight()[goodevent],
        )


    for syst in weights.variations:
        masshist.fill(
            region=region,
            systematic=syst,
            mass=mass,
            weight=weights.weight(syst)[goodevent],
        )


    out = {
    events.metadata["dataset"]: {
        "sumw": ak.sum(events.genWeight),
        "mass": masshist,
        "weightStats": weights.weightStatistics,
    }
    }

