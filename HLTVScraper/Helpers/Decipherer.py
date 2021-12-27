from bs4 import BeautifulSoup as soup
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchDetails import MatchDetails
from Commons.Types.Match.PastMatch import PastMatch

# CONVERT TO A FACTORY WHICH TAKES IN CONTAINER AND CREATES A PAST/CU/FUTURE MATCH
class Decipherer:
    def __init__(self):
        pass

    def validateContainer(self, container: soup.element.Tag):
        if container['class'] not in [MatchContainers.past.value, MatchContainers.present.value,
                                      MatchContainers.future]:
            raise TypeError('Was not able to decipher the given div')

    def getTeams(self, container: soup.element.Tag) -> [str]:
        teamNames = []
        teams = container.find_all(class_="matchTeamName")
        for team in teams:
            teamNames.append(team.getText())
        return teamNames

    def getLinkToGame(self, container: soup.element.Tag) -> str:
        hltvHomePage = "https://www.hltv.org"
        gameLink = hltvHomePage + container.a.get('href')
        return gameLink

    def getBestOf(self, container: soup.element.Tag) -> int:
        self.validateContainer()