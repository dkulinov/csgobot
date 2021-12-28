from bs4 import BeautifulSoup as soup
from Commons.Types.Match.CurrentMatch import CurrentMatch
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails
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
        team1, team2 = self.getTeams(container, MatchDetails.cuTeam)
        team1Logo, team2Logo = self.getTeamLogos(container, MatchDetails.cuLogo)
        link = self.getLinkToGame(container)
        team1CuMapScore, team2CuMapScore = self.getCurrentScore(container)
        team1MapsWon, team2MapsWon = self.getMapScore(container)
        bestOf = self.getBestOf(container)
        return CurrentMatch(team1, team2, team1Logo, team2Logo, link, team1CuMapScore, team2CuMapScore, team1MapsWon, team2MapsWon, bestOf)

    def getMapScore(self, container: soup.element.Tag) -> [int]:
        # TODO: check if correct
        resultContainer = container.find(class_=MatchDetails.cuMapScore).span
        scores = []
        for results in resultContainer.find_all('span'):
            scores.append(int(results.getText()))
        return scores

    def getCurrentScore(self, container: soup.element.Tag) -> [int]:
        # TODO: check
        pass

    def getBestOf(self, container: soup.element.Tag) -> int:
        return int(container.find(class_=MatchDetails.bestOf).getText()[-1])



