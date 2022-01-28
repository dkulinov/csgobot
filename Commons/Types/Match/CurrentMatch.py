from Commons.Types.Match.Match import Match


class CurrentMatch(Match):
    def __init__(self,
                 team1: str, team2: str,
                 team1Logo: str, team2Logo: str, link: str,
                 team1CuMapScore: str, team2CuMapScore: str,
                 team1MapsWon: str, team2MapsWon: str, bestOf: int):
        super().__init__(team1, team2, team1Logo, team2Logo, link)
        self.team1CuMapScore = team1CuMapScore
        self.team2CuMapScore = team2CuMapScore
        self.team1MapsWon = team1MapsWon
        self.team2MapsWon = team2MapsWon
        self.bestOf = bestOf
