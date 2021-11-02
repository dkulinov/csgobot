class TeamDict:

    def __init__(self):
        Teams = {
            "faze": 1
        }

    def getTeamId(self, team: str):
        return self.Teams[team]
