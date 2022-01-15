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
        epochTime = self.getEpochTime(container)
        bestOf = self.getBestOf(container)
        return FutureMatch(team1, team2, team1Logo, team2Logo, link, epochTime, bestOf)

    def getBestOf(self, container: soup.element.Tag) -> int:
        return int(container.find(class_=MatchDetails.bestOf).getText()[-1])

    def getEpochTime(self, container: soup.element.Tag) -> str:
        if container.find(class_=MatchDetails.matchTime).getText() == "LIVE":
            return "LIVE"
        return container.find(class_=MatchDetails.matchTime).get('data-unix')
