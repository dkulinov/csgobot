from enum import Enum


class MatchDetails(Enum):
    pastTeam = "team"
    cuTeam = "matchTeamName"
    futureTeam = "matchTeamName"
    matchTime = "matchTime"
    bestOf = "matchMeta"
    cuScore = "currentMapScore"
    cuMapScore = "mapScore"  # need to go inside this span to get map score
    resultScores = "result-score"
    logo = "matchTeamLogo"
    resultLogo = "team-logo"