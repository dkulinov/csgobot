from bs4 import BeautifulSoup as soup
from Commons.Types.Match.FutureMatch import FutureMatch
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

    def getTeams(self, container: soup.element.Tag) -> [str]:
        pass

    def getBestOf(self, container: soup.element.Tag) -> int:
        pass

    def getDate(self, container: soup.element.Tag):
        pass

    def getTime(self, container: soup.element.Tag):
        pass

    def getTeamLogos(self, container: soup.element.Tag) -> [str]:
        pass
