import datetime
from Commons.Types.MatchStats import MatchStats


class Match:
    date: datetime
    score: str
    team: str
    matchStats: MatchStats
