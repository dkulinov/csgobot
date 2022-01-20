from Commons.Types.SeriesStats import PlayerStats


class MatchStats:
    def __init__(self,
                 team1Stats: [PlayerStats],
                 team2Stats: [PlayerStats],
                 team1Score: int,
                 team2Score: int,
                 mapName: str):
        self.team1Stats = team1Stats
        self.team2Stats = team2Stats
        self.team1Score = team1Score
        self.team2Score = team2Score
        self.mapName = mapName
