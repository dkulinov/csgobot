from Commons.Types.Match.Match import Match


class FutureMatch(Match):
    def __init__(self,
                 team1: str, team2: str,
                 team1Logo: str, team2Logo: str, link: str,
                 epochTime: str, bestOf: int, emptyMatchDescription: str):
        super().__init(team1, team2, team1Logo, team2Logo, link)
        self.epochTime = epochTime
        self.bestOf = bestOf
        self.emptyMatchDescription = emptyMatchDescription
