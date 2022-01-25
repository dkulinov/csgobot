from bs4 import element
from Commons.Types.Match.MatchByTeam import MatchByTeam
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails
from HLTVScraper.Helpers.Factories.MatchFactories.MatchFactory import AbstractMatchFactory
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers


class MatchByTeamFactory(AbstractMatchFactory):
    def __init__(self):
        pass

    def validateContainer(self, container: element.Tag):
        containerClasses: list = container['class']
        if MatchContainers.byTeam.value not in containerClasses:
            raise TypeError("Was not able to create Match by Team from given container.")

    def createMatch(self, container: element.Tag) -> MatchByTeam:
        self.validateContainer(container)
        team1, team2 = self.getTeams(container, MatchDetails.byTeamMatchTeam)
        team1Logo, team2Logo = self.getTeamLogos(container, MatchDetails.byTeamMatchLogo)
        link = self.getLinkToGame(container)
        team1Score, team2Score = self.getScore(container)
        epochTime = self.getEpochTime(container)
        return MatchByTeam(team1, team2, team1Logo, team2Logo, link, team1Score, team2Score, epochTime)

    def getLinkToGame(self, container: element.Tag) -> str:
        hltvHomePage = "https://www.hltv.org"
        link = container.find_all('td')[2].a.get('href')
        gameLink = hltvHomePage + link
        return gameLink

    def getEpochTime(self, container: element.Tag) -> str:
        return container.find(class_=MatchDetails.byTeamMatchTime.value).span.get('data-unix')

    def getScore(self, container: element.Tag) -> [int]:
        scoreContainer = container.find(class_=MatchDetails.byTeamScore.value)
        scores = scoreContainer.find_all('span')
        score1 = scores[0].getText()
        score2 = scores[2].getText()
        return [score1, score2]
