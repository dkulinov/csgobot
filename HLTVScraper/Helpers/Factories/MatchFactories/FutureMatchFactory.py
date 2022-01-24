from bs4 import element
from Commons.Types.Match.FutureMatch import FutureMatch
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails
from HLTVScraper.Helpers.Factories.MatchFactories.MatchFactory import AbstractMatchFactory
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers


class FutureMatchFactory(AbstractMatchFactory):
    def __init__(self):
        pass

    def validateContainer(self, container: element.Tag):
        containerClasses: list = container['class']
        if MatchContainers.future.value not in containerClasses:
            raise TypeError("Was not able to create Future Match from given container.")

    def createMatch(self, container: element.Tag) -> FutureMatch:
        self.validateContainer(container)
        link = self.getLinkToGame(container)
        epochTime = self.getEpochTime(container)
        bestOf = self.getBestOf(container)
        if self.isEmptyMatch(container):
            return FutureMatch(None, None, None, None, link, epochTime, bestOf,
                               self.getEmptyMatchDescription(container))
        team1, team2 = self.getTeams(container, MatchDetails.futureTeam)
        team1Logo, team2Logo = self.getTeamLogos(container, MatchDetails.futureLogo)
        return FutureMatch(team1, team2, team1Logo, team2Logo, link, epochTime, bestOf, None)

    def getBestOf(self, container: element.Tag) -> int:
        return int(container.find(class_=MatchDetails.bestOf.value).getText()[-1])

    def getEpochTime(self, container: element.Tag) -> str:
        if container.find(class_=MatchDetails.matchTime.value).getText() == "LIVE":
            return "LIVE"
        return container.find(class_=MatchDetails.matchTime.value).get('data-unix')

    def isEmptyMatch(self, container: element.Tag) -> bool:
        emptyContainerClasses = container.a.find_all('div', recursive=False)[1]['class']
        if MatchDetails.emptyFutureMatch.value in emptyContainerClasses:
            return True
        return False

    def getEmptyMatchDescription(self, container: element.Tag):
        matchInfoEmptyContainer = container.find(class_=MatchDetails.emptyFutureMatch.value)
        return matchInfoEmptyContainer.span.getText()

    def getTeams(self, container, HLTVTeamClassName):
        self.validateHLTVTeamClassName(HLTVTeamClassName)
        teamNames = []
        teams = container.find_all(class_=HLTVTeamClassName.value)
        for team in teams:
            numOfContainerWithName = len(team.find_all('div')) - 1
            teamContainer = team.find_all('div')[numOfContainerWithName]
            teamNames.append(teamContainer.getText())
        return teamNames
