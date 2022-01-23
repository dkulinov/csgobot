from Commons.Types.Match.Match import Match


class PastMatch(Match):
    def __init__(self,
                 team1: str, team2: str,
                 team1Logo: str, team2Logo: str, link: str,
                 team1Score: int, team2Score: int):
        super().__init__(team1, team2, team1Logo, team2Logo, link)
        self.team1Score = team1Score
        self.team2Score = team2Score
