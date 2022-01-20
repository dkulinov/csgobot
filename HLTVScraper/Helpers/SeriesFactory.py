from bs4 import BeautifulSoup as soup

from Commons.Types.SeriesStats import SeriesStats, MatchStats, PlayerStats


class SeriesFactory:
    def __init__(self):
        pass

    def createSeries(self, theSoup: soup.element.Tag) -> SeriesStats:
        self.validateSoup(theSoup)
        team1Name, team2Name = self.getTeamNames(theSoup)
        team1MapsWon, team2MapsWon = self.getMapsWon(theSoup)
        matches = self.getMatches(theSoup)
        return SeriesStats(matches, team1MapsWon, team2MapsWon, team1Name, team2Name)

    def validateSoup(self, theSoup: soup.element.Tag):
        if theSoup.find(class_="countdown").getText().upper() != "MATCH OVER":
            raise ValueError("The URL provided is incorrect or the match is not yet over")

    def getTeamNames(self, theSoup: soup.element.Tag) -> [str]:
        seriesContainer = theSoup.find(class_="teamsBox")
        teamContainers = seriesContainer.find_all(class_="teamName")
        teamNames = []
        for teamContainer in teamContainers:
            teamNames.append(teamContainer.getText())
        return teamNames

    def getMapsWon(self, theSoup: soup.element.Tag) -> [int]:
        seriesContainer = theSoup.find(class_="teamsBox")
        teamContainers = seriesContainer.find_all(class_="team")
        teamMapsWon = []
        for teamContainer in teamContainers:
            teamMapsWon.append(int(teamContainer.div.div.getText()))
        return teamMapsWon

    def getMatches(self, theSoup: soup.element.Tag) -> [MatchStats]:
        matchStats = []
        mapContainers = theSoup.find_all(class_="mapholder")
        for index, mapContainer in enumerate(mapContainers):
            if "played" in mapContainer.div['class']:
                team1Score, team2Score = self.getMapScores(mapContainer)
                team1Stats, team2Stats = self.getMapStats(index+1, theSoup)
                mapName = self.getMapName(mapContainer)
                matchStats.append(MatchStats(team1Stats, team2Stats, team1Score, team2Score, mapName))

        team1TotalStats, team2TotalStats = self.getMapStats(0, theSoup)
        matchStats.append(MatchStats(team1TotalStats, team2TotalStats, None, None, None))
        return matchStats

    def getMapScores(self, theSoup: soup.element.Tag) -> [int]:
        mapScores = []
        mapScoreContainers = theSoup.find_all(class_="results-team-score")
        for mapScoreContainer in mapScoreContainers:
            mapScores.append(int(mapScoreContainer.getText()))
        return mapScores

    def getMapName(self, theSoup: soup.element.Tag) -> str:
        return theSoup.find(class_="mapname").getText()

    def getMapStats(self, mapNumber, theSoup: soup.element.Tag) -> [[PlayerStats]]:
        mapStats = theSoup.find_all(class_="stats-content")[mapNumber]
        statsByTeam = mapStats.find_all(class_="totalstats")
        team1Rows = statsByTeam[0].tbody.find_all('tr')[1:]
        team2Rows = statsByTeam[1].tbody.find_all('tr')[1:]
        team1Stats = []
        team2Stats = []
        for team1Row in team1Rows:
            team1Stats.append(self.createPlayerStats(team1Row))
        for team2Row in team2Rows:
            team2Stats.append(self.createPlayerStats(team2Row))
        return [team1Stats, team2Stats]

    def createPlayerStats(self, row: soup.element.Tag) -> PlayerStats:
        player = row.find(class_="player-nick").getText()
        kill_death = row.find(class_="kd").getText()
        plus_minus = row.find(class_="plus-minus").span.getText()
        avg_damage_per_round = row.find(class_="adr").getText()
        kill_assist_survive_traded = row.find(class_="kast").getText()
        rating = row.find(class_="rating").getText()
        return PlayerStats(player, kill_death, plus_minus, avg_damage_per_round, kill_assist_survive_traded, rating)



    def getPlayerName(self, row: soup.element.Tag) -> str:
        soup

