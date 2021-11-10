class HLTVTeams:

    def __init__(self):
        self.HLTV_teams = {
            "natus-vincere":     4608
            "gambit":            6651,
            "g2":                5995,
            "heroic":            7175,
            "furia":             8297,
            "copenhagen-flames": 7461
            "vitality":          9565,
            "faze":              6667,
            "mouz":              4494,
            "virtuspro":         5378,
            "liquid":            5973,
            "entropiq":          10831,
            "nip":               4411,
            "astralis":          6665,
            "evil-geniuses":     10399,
            "ence":              4869,
            "og":                10503,
            "big":               7532,
            "movistar-riders":   7718,
            "fiend":             11066,
            "spirit":            7020,
            "mad-lions":         8362,
            "forze":             8135,
            "godsent":           6902,
            "skade":             10386,
            "lyngby-vikings":    8963,
            "sinners":           10577,
            "complexity":        5005,
            "dignitas":          5422,
            "dbl-poney":         11003,
            "fnatic":            4991,
            "party-astronauts":  8038,
            "bad-news-bears":    9799,
            "extra-salt":        10948,
            "triumph":           10304,
            "mythic":            5479,
            "pain":              4773,
            "teamone":           6947,
            "9z":                9996,
            "sharks":            8113,
            "00nation":          11309,
            "mibr":              9215,
            "anonymo":           10973,
            "endpoint":          7234,
            "ldlc":              4674,
            "k23":               7244,
            "singularity":       6978,
            "tyloo":             4863,
            "renegades":         6211
        }

    def getTeamId(self, team: str):
        return self.inputTeams[team]

    def getIsValid(self, team: str):
        return team in self.HLTV_teams.keys()
