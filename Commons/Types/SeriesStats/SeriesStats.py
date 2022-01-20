from Commons.Types.SeriesStats import MatchStats


class SeriesStats:
    def __init__(self,
                 matches: [MatchStats],
                 team1MapsWon: int,
                 team2MapsWon: int,
                 team1Name: str,
                 team2Name: str):
        self.matches = matches
        self.team1MapsWon = team1MapsWon
        self.team2MapsWon = team2MapsWon
        self.team1Name = team1Name
        self.team2Name = team2Name
