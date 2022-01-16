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
from datetime import timedelta
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

    # TODO: maybe only do max last week in the past
    def getMatchesByDay(self, theDate: str) -> [Match]:
        lookForDate = self.mapToDate(theDate)
        todayDate = datetime.today().date()
        weekBefore = datetime.today().date() - timedelta(days=7)
        self.validateDateNotMoreThanWeekBefore(lookForDate, weekBefore)
        correctFactory, url = self.getCorrectFactoryAndUrlByDay(lookForDate, todayDate)
        theSoup = self.soupChef.makeSoup(url)
        # TODAY: liveMatchesSection + an upcomingMatchesSection
        # FUTURE: an upcomingMatchesSection
        # PAST: results-sublist. result page shows 100 matches (url: /results?offset=200) means 201-300

    # by day and by team
    # def getPastMatches(predefinedFilter: MatchType, team: str= "None") -> [Match]:
    #     return [Match()]

    # def getStats(team1, team2) -> MatchStats:
    #     return MatchStats()

    def getMatches(self, containerType: MatchContainers, offset: int = 0, numberPast: int = 20,
                   predefinedFilter: MatchType = MatchType.TopTier):
        self.validateNumPastMatches(numberPast)
        correctFactory = self.getCorrectFactory(containerType)
        correctUrl = self.getCorrectMatchesUrl(containerType, predefinedFilter, offset)
        matches = []
        theSoup = self.soupChef.makeSoup(correctUrl)
        matchContainers = theSoup.find_all(class_=containerType)

        for count, matchContainer in enumerate(matchContainers):
            if containerType == MatchContainers.past and count > numberPast:
                break
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

    def getCorrectMatchesUrl(self, containerType: MatchContainers, predefinedFilter: MatchType, offset: int):
        match containerType:
            case MatchContainers.past:
                return self.urlBuilder.buildGetPastMatches(offset)
            case MatchContainers.present:
                return self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
            case MatchContainers.future:
                return self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
            case _:
                raise TypeError("containerType has to be of type MatchContainer")

    def getCorrectFactoryAndUrlByDay(self, lookForDate, todayDate):
        if lookForDate < todayDate:
            return self.pastMatchFactory, self.urlBuilder.buildGetPastMatches()
        elif lookForDate == todayDate:
            return self.currentMatchFactory, self.urlBuilder.buildGetUpcomingMatchesUrl()
        elif lookForDate > todayDate:
            return self.futureMatchFactory, self.urlBuilder.buildGetUpcomingMatchesUrl()

    def mapToDate(self, theDate: str):
        try:
            return datetime.strptime(theDate, "%m/%d/%Y").date()
        except ValueError:
            raise ValueError("Date has to be in the mm/dd/yyyy format.")

    def validateDateNotMoreThanWeekBefore(self, lookForDate, weekBeforeToday):
        weekBeforeLookForDate = lookForDate - timedelta(days=7)
        if weekBeforeLookForDate < weekBeforeToday:
            raise ValueError("Cannot look up matches more than a week before today.")

    def validateNumPastMatches(self, numberPast: int):
        if numberPast > 100:
            raise ValueError("Cannot get more than 100 past matches at a time. Please modify the offset if you want "
                             "to go further into the past")