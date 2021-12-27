from bs4 import BeautifulSoup as soup
from Commons.Types.Match.CurrentMatch import CurrentMatch
from HLTVScraper.Helpers.MatchFactories.MatchFactory import AbstractMatchFactory
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers


class CurrentMatchFactory(AbstractMatchFactory):
    def __init__(self):
        pass

    def validateContainer(self, container: soup.element.Tag):
        if container['class'] != MatchContainers.present.value:
            raise TypeError("Was not able to create Current Match from given container.")

    def createMatch(self, container: soup.element.Tag) -> CurrentMatch:
        self.validateContainer(container)
        team1, team2 = self.getTeams(container)
        team1Logo, team2Logo = self.getTeamLogos(container)
        link = self.getLinkToGame(container)
        team1CuMapScore, team2CuMapScore = self.getCurrentScore(container)
        team1MapsWon, team2MapsWon = self.getMapScore(container)
        bestOf = self.getBestOf(container)
        return CurrentMatch(team1, team2, team1Logo, team2Logo, link, team1CuMapScore, team2CuMapScore, team1MapsWon, team2MapsWon, bestOf)

    def getTeams(self, container: soup.element.Tag) -> [str]:
        pass

    def getMapScore(self, container: soup.element.Tag) -> [int]:
        pass

    def getCurrentScore(self, container: soup.element.Tag) -> [int]:
        pass

    def getBestOf(self, container: soup.element.Tag) -> int:
        pass

    def getTeamLogos(self, container: soup.element.Tag) -> [str]:
        pass
