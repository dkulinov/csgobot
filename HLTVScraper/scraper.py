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
from HLTVScraper.Helpers.MatchFactories.MatchFactory import AbstractMatchFactory
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
        correctFactory = self.getCorrectFactory(containerType)
        url = self.urlBuilder.buildGetMatchesByTeamUrl(team)

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
        correctFactory = self.getCorrectFactory(containerType)
        correctUrl = self.getCorrectMatchesUrl(containerType, predefinedFilter)
        matches = []
        theSoup = self.soupChef.makeSoup(correctUrl)
        matchContainers = theSoup.find_all(class_=containerType)

        for matchContainer in matchContainers:
            matches.append(correctFactory.createMatch(matchContainer))

        return matches

    def getCorrectFactory(self, containerType: MatchContainers) -> AbstractMatchFactory:
        match containerType:
            case MatchContainers.past:
                return self.pastMatchFactory
            case MatchContainers.present:
                return self.currentMatchFactory
            case MatchContainers.future:
                return self.futureMatchFactory
            case _:
                raise TypeError("containerType has to be of type MatchContainer")

    def getCorrectMatchesUrl(self, containerType: MatchContainers, predefinedFilter: MatchType):
        match containerType:
            case MatchContainers.past:
                return self.urlBuilder.buildGetPastMatches()
            case MatchContainers.present:
                return self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
            case MatchContainers.future:
                return self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
            case _:
                raise TypeError("containerType has to be of type MatchContainer")