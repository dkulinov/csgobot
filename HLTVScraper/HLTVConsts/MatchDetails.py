from enum import Enum


class MatchDetails(Enum):
    pastTeam = "team"
    cuTeam = "matchTeamName"
    futureTeam = "matchTeamName"
    byTeamMatchTeam = "team-name"
    pastLogo = "team-logo"
    cuLogo = "matchTeamLogo"
    futureLogo = 'matchTeamLogo'
    byTeamMatchLogo = "team-logo"
    matchTime = "matchTime"
    byTeamMatchTime = "date-cell"
    bestOf = "matchMeta"
    cuScore = "currentMapScore"
    cuMapScore = "mapScore"
    pastMapScore = "result-score"
    byTeamScore = "score-cell"
