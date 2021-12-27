from bs4 import BeautifulSoup as soup
from Commons.Types.Match.Match import Match


class AbstractMatchFactory:
    def __init__(self):
        pass

    def validateContainer(self, container: soup.element.Tag):
        pass

    def createMatch(self, container) -> Match:
        pass

    def getLinkToGame(self, container: soup.element.Tag) -> str:
        hltvHomePage = "https://www.hltv.org"
        gameLink = hltvHomePage + container.a.get('href')
        return gameLink

    def getTeams(self, container, HLTVTeamClassName):
        self.validateHLTVTeamClassName(HLTVTeamClassName)
        teamNames = []
        teams = container.find_all(class_=HLTVTeamClassName)
        for team in teams:
            teamNames.append(team.getText())
        return teamNames

    def validateHLTVTeamClassName(self, HLTVTeamClassName):
        if HLTVTeamClassName not in [MatchDetails.resultTeam, MatchDetails.cuOrFutureTeam]:
            raise TypeError("Invalid team class name:", HLTVTeamClassName)
