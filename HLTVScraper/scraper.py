from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

from Commons.Types.Match import PastMatch, FutureMatch
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
        self.validateDateNotMoreThanWeekBefore(lookForDate)
        url = self.getMatchesByDayUrl(lookForDate, todayDate)
        theSoup = self.soupChef.makeSoup(url)
        matches = []
        if lookForDate < todayDate:
            matches = self.getPastMatchesByDay(lookForDate)
        elif lookForDate == todayDate:
            matches = self.getTodaysMatches(theSoup)
        elif lookForDate > todayDate:
            matches = self.getFutureMatchesByDay(theSoup, lookForDate)
        return matches

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

    def getMatchesByDayUrl(self, lookForDate, todayDate):
        if lookForDate < todayDate:
            return self.urlBuilder.buildGetPastMatches()
        elif lookForDate == todayDate:
            return self.urlBuilder.buildGetUpcomingMatchesUrl()
        elif lookForDate > todayDate:
            return self.urlBuilder.buildGetUpcomingMatchesUrl()

    def mapToDate(self, theDate: str):
        try:
            return datetime.strptime(theDate, "%m/%d/%Y").date()
        except ValueError:
            raise ValueError("Date has to be in the mm/dd/yyyy format.")

    def validateDateNotMoreThanWeekBefore(self, lookForDate):
        weekBeforeToday = datetime.today().date() - timedelta(days=7)
        if lookForDate < weekBeforeToday:
            raise ValueError("Cannot look up matches more than a week before today.")

    def validateNumPastMatches(self, numberPast: int):
        if numberPast > 100:
            raise ValueError("Cannot get more than 100 past matches at a time. Please modify the offset if you want "
                             "to go further into the past")

    def getPastMatchesByDay(self, lookForDate) -> [PastMatch]:
        maxDays = 7
        daysSearched = 0
        soups = []
        offset = 0
        while daysSearched < maxDays:
            url = self.urlBuilder.buildGetPastMatches(offset)
            soup = self.soupChef.makeSoup(url)
            dayResultContainers = soup.find_all(class_="results-sublist")
            soups.append(dayResultContainers)
            daysSearched += len(dayResultContainers)
            offset += 100
            lastDayTitle = dayResultContainers[-1].div.getText()
            while daysSearched == maxDays:
                url = self.urlBuilder.buildGetPastMatches(offset)
                soup = self.soupChef.makeSoup(url)
                dayResultContainers = soup.find_all(class_="result-sublist")
                soups.append(dayResultContainers[0])
                offset += 100
                if dayResultContainers[-1].div.getText() != lastDayTitle:
                    daysSearched += 1
        soupsToSearch = []
        for theSoup in soups:
            dateFromTitle = theSoup.div.getText()[12:]
            dateAsArray = dateFromTitle.split(" ")
            dateAsArray[1] = dateAsArray[1][:2]
            theDate = "".join(dateAsArray)
            if theDate == lookForDate:
                soupsToSearch.append(theSoup)
        matches = []
        for soupToSearch in soupsToSearch:
            correctFactory = self.pastMatchFactory
            matchContainers = soupToSearch.find_all(class_=MatchContainers.past)
            for matchContainer in matchContainers:
                matches.append(correctFactory.createMatch(matchContainer))
        return matches

    def getFutureMatchesByDay(self, soup, lookForDate) -> [FutureMatch]:
        matches = []
        correctMatchDay = self.getCorrectFutureMatchDay(soup, lookForDate)
        matchContainers = correctMatchDay.find_all(class_=MatchContainers.future)
        for matchContainer in matchContainers:
            matches.append(self.futureMatchFactory.createMatch(matchContainer))
        return matches

    def getTodaysMatches(self, soup) -> [Match]:
        liveMatches = self.getMatches(MatchContainers.present, predefinedFilter=None)
        todayDate = datetime.today().date()
        upcomingTodayMatches = self.getFutureMatchesByDay(soup, todayDate)
        return liveMatches + upcomingTodayMatches

    def getCorrectFutureMatchDay(self, soup, lookForDate):
        matchDays = soup.find_all(class_="upcomingMatchesSection")
        correctMatchDay = None
        for matchDay in matchDays:
            matchDayDate = self.mapToDate(matchDay.div.getText()[-10:])
            if matchDayDate == lookForDate:
                correctMatchDay = matchDay
                break
        if not correctMatchDay:
            raise ValueError("Could not find matches for ", lookForDate)
        return correctMatchDay
