from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from Commons.Types.MatchType import MatchType
from Commons.Types.Match.Match import Match
from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Mappers.InputToHtlvTeam import mapInputToCorrectHltvTeam
from HLTVScraper.Helpers import UrlBuilder
from HLTVScraper.Helpers.MatchFactories.CurrentMatchFactory import CurrentMatchFactory
from HLTVScraper.Helpers.MatchFactories.FutureMatchFactory import FutureMatchFactory
from HLTVScraper.Helpers.MatchFactories.PastMatchFactory import PastMatchFactory


class Scraper:
    def __init__(
            self,
            urlBuilder: UrlBuilder,
            pastMatchFactory: PastMatchFactory,
            currentMatchFactory: CurrentMatchFactory,
            futureMatchFactory: FutureMatchFactory
    ):
        self.urlBuilder = urlBuilder
        self.pastMatchFactory = pastMatchFactory
        self.currentMatchFactory = currentMatchFactory
        self.futureMatchFactory = futureMatchFactory

    def getUpcomingMatches(self, predefinedFilter: MatchType = MatchType.TopTier) -> [Match]:
        url = self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
        headers = self.urlBuilder.getHeaders()
        req = Request(url, headers=headers)
        res = urlopen(req)
        html = res.read()

        theSoup = soup(html, "html.parser")
        matchesByDay = theSoup.find(class_='upcomingMatchesContainer')
        sectionClassname = matchesByDay.div.get('data-zonedgrouping-group-classes')
        dateClassname = matchesByDay.div.get('data-zonedgrouping-headline-classes')
        for teamName in theSoup.find_all(class_="matchTeamName"):
            print(teamName.getText())
        # print(matchesByDay)
        # team1s = theSoup.find_all(class_='team1')
        # team2s = theSoup.find_all(class_='team2')
        # numMatches = len(team1s)
        # for i in range(numMatches):
        #     print("\nMatch: " + team1s[i].get_text().strip() + " vs " + team2s[i].get_text().strip())

        # for child in theSoup.contents[2].contents:
        #     if(child.contents.contains())
        #     print("CHILD: ", child)
        return [Match()]

    def getUpcomingMatchesByTeam(self, team: str) -> [Match]:
        try:
            validTeam = mapInputToCorrectHltvTeam(team)
        except InvalidTeamException as err:
            return str(err)
        pass

    def getUpcomingMatchesByDay(self, day: str) -> [Match]:
        pass

    # by day and by team
    # def getPastMatches(predefinedFilter: MatchType, team: str= "None") -> [Match]:
    #     return [Match()]
    #
    # def getCurrentMatches(predefinedFilter: MatchType, team:str = "None") -> [Match]:
    #     return [Match()]
    #
    # def getStats(team1, team2) -> MatchStats:
    #     return MatchStats()
