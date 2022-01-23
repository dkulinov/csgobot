from bs4 import element
from Commons.Types.Match.PastMatch import PastMatch
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails
from HLTVScraper.Helpers.Factories.MatchFactories.MatchFactory import AbstractMatchFactory


class PastMatchFactory(AbstractMatchFactory):
    def __init__(self):
        pass

    def validateContainer(self, container: element.Tag):
        containerClass: list = container['class']
        try:
            containerClass.index(MatchContainers.past.value)
        except ValueError:
            raise TypeError("Was not able to create Past Match from given container.")

    def createMatch(self, container: element.Tag) -> PastMatch:
        self.validateContainer(container)
        print(container.prettify())
        team1, team2 = self.getTeams(container, MatchDetails.pastTeam)
        team1Logo, team2Logo = self.getTeamLogos(container, MatchDetails.pastLogo)
        link = self.getLinkToGame(container)
        team1Score, team2Score = self.getMapScore(container)
        return PastMatch(team1, team2, team1Logo, team2Logo, link, team1Score, team2Score)

    def getMapScore(self, container: element.Tag) -> [int]:
        resultContainer = container.find(class_=MatchDetails.pastMapScore.value)
        scores = []
        for results in resultContainer.find_all('span'):
            scores.append(int(results.getText()))
        return scores

