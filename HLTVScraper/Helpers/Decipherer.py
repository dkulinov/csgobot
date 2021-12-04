from bs4 import BeautifulSoup as soup
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers


class Decipherer:
    def __init__(self):
        pass

    def validateContainer(container: soup.element.Tag):
        if container['class'] not in [MatchContainers.past.value, MatchContainers.present.value,
                                      MatchContainers.future]:
            raise TypeError('Was not able to decipher the given div')

    def getTeams(self, container: soup.element.Tag):
        self.validateContainer(container)

    def getLinkToGame(self, container: soup.element.Tag) -> str:
        self.validateContainer(container)
        hltvHomePage = "https://www.hltv.org"
        gameLink = hltvHomePage + container.a.get('href')
        return gameLink
