from enum import Enum


class MatchDetails(Enum):
    cuOrFutureTeam = "matchTeamName"
    matchTime = "matchTime"
    bestOf = "matchMeta"
    cuScore = "currentMapScore"
    cuMapScore = "mapScore"  # need to go inside this span to get map score
    resultTeam = "team"
    resultScores = "result-score"
