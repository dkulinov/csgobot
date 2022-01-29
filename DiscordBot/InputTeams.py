from Commons.Types.Team import HLTVTeams

common_team_nicknames = {
    "natus vincere",
    "navi",
    "cph-flames",
    "copenhagen flames",
    "cph flames",
    "mouz-sports",
    "mouz sports",
    "vp",
    "virtus.pro",
    "virtus pro",
    "virtus-pro",
    "tl",
    "eg",
    "evil geniuses",
    "movistar riders",
    "movistar",
    "mad lions",
    "lyngby vikings",
    "sinners",
    "dbl poney",
    "party astronauts",
    "partynauts",
    "bnb",
    "bad news bears",
    "extra salt",
    "es",
}


def getIsValid(team: str):
    validInputTeams = set.union(common_team_nicknames, list(HLTVTeams().HLTV_teams.keys()))
    return team in validInputTeams
