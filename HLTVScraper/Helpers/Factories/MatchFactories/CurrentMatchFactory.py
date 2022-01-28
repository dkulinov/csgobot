from time import sleep

from bs4 import element
from Commons.Types.Match.CurrentMatch import CurrentMatch
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails
from HLTVScraper.Helpers.Factories.MatchFactories.MatchFactory import AbstractMatchFactory


class CurrentMatchFactory(AbstractMatchFactory):
    def __init__(self):
        pass

    def validateContainer(self, container: element.Tag):
        containerClasses: list = container['class']
        if MatchContainers.present.value not in containerClasses:
            raise TypeError("Was not able to create Current Match from given container.")

    def createMatch(self, container: element.Tag) -> CurrentMatch:
        self.validateContainer(container)
        team1, team2 = self.getTeams(container, MatchDetails.cuTeam)
        team1Logo, team2Logo = self.getTeamLogos(container, MatchDetails.cuLogo)
        link = self.getLinkToGame(container)
        team1CuMapScore, team2CuMapScore = self.getCurrentScore(container)
        team1MapsWon, team2MapsWon = self.getMapScore(container)
        bestOf = self.getBestOf(container)
        return CurrentMatch(team1, team2, team1Logo, team2Logo, link, team1CuMapScore, team2CuMapScore, team1MapsWon, team2MapsWon, bestOf)

    def getMapScore(self, container: element.Tag) -> [int]:
        resultContainers = container.find_all(class_=MatchDetails.cuMapScore.value)
        scores = []
        for result in resultContainers:
            scores.append(result.span.getText().strip())
        return scores

    def getCurrentScore(self, container: element.Tag) -> [int]:
        scores = []
        for score in container.find_all(class_=MatchDetails.cuScore.value):
            scores.append(score.getText().strip())
        return scores

    def getBestOf(self, container: element.Tag) -> int:
        return int(container.find(class_=MatchDetails.bestOf.value).getText()[-1])



