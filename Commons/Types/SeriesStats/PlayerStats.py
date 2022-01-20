class PlayerStats:
    def __init__(self,
                 player: str,
                 kill_death: str,
                 plus_minus: str,
                 avg_damage_per_round: str,
                 kill_assist_survive_traded: str,
                 rating: str
                 ):
        self.player = player
        self.kill_death = kill_death
        self.plus_minus = plus_minus
        self.avg_damage_per_round = avg_damage_per_round
        self.kill_assist_survive_traded = kill_assist_survive_traded
        self.rating = rating
