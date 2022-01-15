from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from Commons.Types.MatchType import MatchType
from Commons.Types.Match.Match import Match
from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Mappers.InputToHtlvTeam import mapInputToCorrectHltvTeam
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchTIme import MatchTime
from HLTVScraper.Helpers import UrlBuilder, SoupChef
from HLTVScraper.Helpers.MatchFactories.CurrentMatchFactory import CurrentMatchFactory
from HLTVScraper.Helpers.MatchFactories.FutureMatchFactory import FutureMatchFactory
from HLTVScraper.Helpers.MatchFactories.MatchByTeamFactory import MatchByTeamFactory
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
            futureMatchFactory: FutureMatchFactory,
            matchByTeamFactory: MatchByTeamFactory
    ):
        self.urlBuilder = urlBuilder
        self.pastMatchFactory = pastMatchFactory
        self.currentMatchFactory = currentMatchFactory
        self.futureMatchFactory = futureMatchFactory
        self.matchByTeamFactory = matchByTeamFactory
        self.soupChef = soupChef

    def getMatchesByTeam(self, team: str, timeFrame: MatchTime = MatchTime.future.value) -> [Match]:
        url = self.urlBuilder.buildGetMatchesByTeamUrl(team)
        theSoup = self.soupChef.makeSoup(url).find_all(class_="match-table")[timeFrame.value]
        matches = []
        matchContainers = theSoup.find_all(class_=MatchContainers.byTeam)

        for matchContainer in matchContainers:
            matches.append(self.matchByTeamFactory.createMatch(matchContainer))

        return matches


    def getMatchesByDay(self, theDate: str) -> [Match]:
        correctFactory = None
        correctUrl = None
        try:
            lookForDate = datetime.strptime(theDate, "%m/%d/%Y").date()
        except ValueError:
            raise ValueError("Date has to be in the mm/dd/yyyy format.")
        todayDate = datetime.today().date()
        if lookForDate < todayDate:
            correctFactory = self.pastMatchFactory
            correctUrl = self.urlBuilder.buildGetPastMatches()
        elif lookForDate == todayDate:
            correctFactory = self.currentMatchFactory
            correctUrl = self.urlBuilder.buildGetUpcomingMatchesUrl()
        elif lookForDate > todayDate:
            correctFactory = self.futureMatchFactory
            correctUrl = self.urlBuilder.buildGetUpcomingMatchesUrl()


    # by day and by team
    # def getPastMatches(predefinedFilter: MatchType, team: str= "None") -> [Match]:
    #     return [Match()]


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