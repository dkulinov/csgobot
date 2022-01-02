from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from Commons.Types.MatchType import MatchType
from Commons.Types.Match.Match import Match
from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Mappers.InputToHtlvTeam import mapInputToCorrectHltvTeam
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.Helpers import UrlBuilder, SoupChef
from HLTVScraper.Helpers.MatchFactories.CurrentMatchFactory import CurrentMatchFactory
from HLTVScraper.Helpers.MatchFactories.FutureMatchFactory import FutureMatchFactory
from HLTVScraper.Helpers.MatchFactories.PastMatchFactory import PastMatchFactory
from datetime import datetime
import time


class Scraper:
    def __init__(
            self,
            urlBuilder: UrlBuilder,
            soupChef: SoupChef,
            pastMatchFactory: PastMatchFactory,
            currentMatchFactory: CurrentMatchFactory,
            futureMatchFactory: FutureMatchFactory
    ):
        self.urlBuilder = urlBuilder
        self.pastMatchFactory = pastMatchFactory
        self.currentMatchFactory = currentMatchFactory
        self.futureMatchFactory = futureMatchFactory
        self.soupChef = soupChef

    def getMatchesByTeam(self, team: str, containerType: MatchContainers) -> [Match]:
        correctFactory = None
        url = self.urlBuilder.buildGetMatchesByTeamUrl(team)
        # TODO: turn into switch statement
        if containerType == MatchContainers.past:
            correctFactory = self.pastMatchFactory
        elif containerType == MatchContainers.present:
            correctFactory = self.currentMatchFactory
        elif containerType == MatchContainers.future:
            correctFactory = self.futureMatchFactory
        if correctFactory is None:
            raise TypeError("containerType has to be of type MatchContainer")



    def getUpcomingMatchesByDay(self, timestamp: str) -> [Match]:
        datetime.fromtimestamp(timestamp)
        time.time()
        pass

    # by day and by team
    # def getPastMatches(predefinedFilter: MatchType, team: str= "None") -> [Match]:
    #     return [Match()]
    #
    #
    # def getStats(team1, team2) -> MatchStats:
    #     return MatchStats()

    def getMatches(self, containerType: MatchContainers, predefinedFilter: MatchType = MatchType.TopTier):

        correctFactory = None
        correctUrl = None
        # TODO: turn into switch statement
        if containerType == MatchContainers.past:
            correctFactory = self.pastMatchFactory
            correctUrl = self.urlBuilder.buildGetPastMatches()
        elif containerType == MatchContainers.present:
            correctFactory = self.currentMatchFactory
            correctUrl = self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
        elif containerType == MatchContainers.future:
            correctFactory = self.futureMatchFactory
            correctUrl = self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
        if correctFactory is None or correctUrl is None:
            raise TypeError("containerType has to be of type MatchContainer")

        matches = []
        theSoup = self.soupChef.makeSoup(correctUrl)
        matchContainers = theSoup.find_all(class_=containerType)

        for matchContainer in matchContainers:
            matches.append(correctFactory.createMatch(matchContainer))

        return matches


