from bs4 import BeautifulSoup as soup
from Commons.Types.Match.Match import Match
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails


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

    def getTeamLogos(self, container, HLTVTeamLogoClassName):
        self.validateHLTVTeamLogoClassName(HLTVTeamLogoClassName)
        teamLogoLinks = []
        teamLogos = container.find_all(class_=HLTVTeamLogoClassName)
        for teamLogo in teamLogos:
            teamLogoLinks.append(teamLogo.get('src'))
        return teamLogoLinks

    def validateHLTVTeamClassName(self, HLTVTeamClassName):
        if HLTVTeamClassName not in [MatchDetails.pastTeam, MatchDetails.cuTeam, MatchDetails.futureTeam, MatchDetails.byTeamMatchTeam]:
            raise TypeError("Invalid team class name:", HLTVTeamClassName)

    def validateHLTVTeamLogoClassName(self, HLTVTeamLogoClassName):
        if HLTVTeamLogoClassName not in [MatchDetails.pastLogo, MatchDetails.cuLogo, MatchDetails.futureLogo, MatchDetails.byTeamMatchLogo]:
            raise TypeError("Invalid team logo class name:", HLTVTeamLogoClassName)