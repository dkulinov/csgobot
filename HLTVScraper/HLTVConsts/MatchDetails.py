from enum import Enum


class MatchDetails(Enum):
    pastTeam = "team"
    cuTeam = "matchTeamName"
    futureTeam = "matchTeamName"
    pastLogo = "team-logo"
    cuLogo = "matchTeamLogo"
    futureLogo = 'matchTeamLogo'
    matchTime = "matchTime"
    bestOf = "matchMeta"
    cuScore = "currentMapScore"
    cuMapScore = "mapScore"  # need to go inside this span to get map score
    pastMapScore = "result-score"
