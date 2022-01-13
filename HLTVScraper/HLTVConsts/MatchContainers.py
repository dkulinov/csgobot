from enum import Enum


class MatchContainers(Enum):
    past = "result-con"
    present = "liveMatch"
    future = "upcomingMatch"
    byTeam = "team-row"


