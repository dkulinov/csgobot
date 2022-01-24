from bs4 import element
from Commons.Types.Match.Match import Match
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails


class AbstractMatchFactory:
    def __init__(self):
        pass

    def validateContainer(self, container: element.Tag):
        pass

    def createMatch(self, container) -> Match:
        pass

    def getLinkToGame(self, container: element.Tag) -> str:
        hltvHomePage = "https://www.hltv.org"
        gameLink = hltvHomePage + container.a.get('href')
        return gameLink

    def getTeams(self, container, HLTVTeamClassName):
        self.validateHLTVTeamClassName(HLTVTeamClassName)
        teamNames = []
        teams = container.find_all(class_=HLTVTeamClassName.value)
        for team in teams:
            teamNames.append(team.getText())
        return teamNames

    def getTeamLogos(self, container, HLTVTeamLogoClassName):
        self.validateHLTVTeamLogoClassName(HLTVTeamLogoClassName)
        teamLogoLinks = []
        teamLogos = container.find_all(class_=HLTVTeamLogoClassName.value)
        teamLogoLinks.append(teamLogos[0].get('src'))
        if len(teamLogos) > 1:
            teamLogoLinks.append(teamLogos[-1].get('src'))
        else:
            teamLogoLinks.append("")
        return teamLogoLinks

    def validateHLTVTeamClassName(self, HLTVTeamClassName):
        if HLTVTeamClassName not in [MatchDetails.pastTeam, MatchDetails.cuTeam, MatchDetails.futureTeam, MatchDetails.byTeamMatchTeam]:
            raise TypeError("Invalid team class name:", HLTVTeamClassName)

    def validateHLTVTeamLogoClassName(self, HLTVTeamLogoClassName):
        if HLTVTeamLogoClassName not in [MatchDetails.pastLogo, MatchDetails.cuLogo, MatchDetails.futureLogo, MatchDetails.byTeamMatchLogo]:
            raise TypeError("Invalid team logo class name:", HLTVTeamLogoClassName)