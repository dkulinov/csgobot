from bs4 import BeautifulSoup as soup
from Commons.Types.Match.PastMatch import PastMatch
from HLTVScraper.Helpers.MatchFactories.MatchFactory import AbstractMatchFactory
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers


class PastMatchFactory(AbstractMatchFactory):
    def __init__(self):
        pass

    def validateContainer(self, container: soup.element.Tag):
        if container['class'] != MatchContainers.past.value:
            raise TypeError("Was not able to create Past Match from given container.")

    def createMatch(self, container: soup.element.Tag) -> PastMatch:
        self.validateContainer(container)
        team1, team2 = self.getTeams(container)
        team1Logo, team2Logo = self.getTeamLogos(container)
        link = self.getLinkToGame(container)
        team1Score, team2Score = self.getMapScore(container)
        return PastMatch(team1, team2, team1Logo, team2Logo, link, team1Score, team2Score)

    def getTeams(self, container: soup.element.Tag) -> [str]:
        pass

    def getMapScore(self, container: soup.element.Tag) -> [int]:
        pass

    def getTeamLogos(self, container: soup.element.Tag) -> [str]:
        pass