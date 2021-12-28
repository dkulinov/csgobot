from bs4 import BeautifulSoup as soup
from Commons.Types.Match.FutureMatch import FutureMatch
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails
from HLTVScraper.Helpers.MatchFactories.MatchFactory import AbstractMatchFactory
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers


class FutureMatchFactory(AbstractMatchFactory):
    def __init__(self):
        pass

    def validateContainer(self, container: soup.element.Tag):
        if container['class'] != MatchContainers.future.value:
            raise TypeError("Was not able to create Past Match from given container.")

    def createMatch(self, container: soup.element.Tag) -> FutureMatch:
        self.validateContainer(container)
        team1, team2 = self.getTeams(container, MatchDetails.futureTeam)
        team1Logo, team2Logo = self.getTeamLogos(container, MatchDetails.futureLogo)
        link = self.getLinkToGame(container)
        date = self.getDate(container)
        time = self.getTime(container)
        bestOf = self.getBestOf(container)
        return FutureMatch(team1, team2, team1Logo, team2Logo, link, date, time, bestOf)


    def getBestOf(self, container: soup.element.Tag) -> int:
        pass

    def getDate(self, container: soup.element.Tag):
        pass

    def getTime(self, container: soup.element.Tag):
        pass

