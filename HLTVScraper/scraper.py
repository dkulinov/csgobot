from bs4 import BeautifulSoup as soup
from Commons.Types.Match import PastMatch, FutureMatch
from Commons.Types.MatchType import MatchType
from Commons.Types.Match.Match import Match
from Commons.Types.SeriesStats import SeriesStats
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchTIme import MatchTime
from HLTVScraper.Helpers import UrlBuilder, SoupChef, SeriesFactory, NewsFactory
from HLTVScraper.Helpers.MatchFactories.CurrentMatchFactory import CurrentMatchFactory
from HLTVScraper.Helpers.MatchFactories.FutureMatchFactory import FutureMatchFactory
from HLTVScraper.Helpers.MatchFactories.MatchByTeamFactory import MatchByTeamFactory
from HLTVScraper.Helpers.MatchFactories.MatchFactory import AbstractMatchFactory
from HLTVScraper.Helpers.MatchFactories.PastMatchFactory import PastMatchFactory
from datetime import datetime
from datetime import timedelta


class Scraper:
    def __init__(
            self,
            urlBuilder: UrlBuilder,
            soupChef: SoupChef,
            pastMatchFactory: PastMatchFactory,
            currentMatchFactory: CurrentMatchFactory,
            futureMatchFactory: FutureMatchFactory,
            seriesFactory: SeriesFactory,
            matchByTeamFactory: MatchByTeamFactory,
            newsFactory: NewsFactory,
    ):
        self.urlBuilder = urlBuilder
        self.pastMatchFactory = pastMatchFactory
        self.currentMatchFactory = currentMatchFactory
        self.futureMatchFactory = futureMatchFactory
        self.matchByTeamFactory = matchByTeamFactory
        self.seriesFactory = seriesFactory
        self.soupChef = soupChef
        self.newsFactory = newsFactory

    def getMatchesFromSoup(self, theSoup: soup.element.Tag, containerType: MatchContainers):
        matches = []
        correctFactory = self.getCorrectFactory(containerType)
        matchContainers = theSoup.find_all(class_=containerType)
        for matchContainer in matchContainers:
            matches.append(correctFactory.createMatch(matchContainer))
        return matches

    def getMatchesByTeam(self, team: str, timeFrame: MatchTime = MatchTime.future.value) -> [Match]:
        url = self.urlBuilder.buildGetMatchesByTeamUrl(team)
        theSoup = self.soupChef.makeSoup(url).find_all(class_="match-table")[timeFrame.value]
        return self.getMatchesFromSoup(theSoup, MatchContainers.byTeam)

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

    def getAllMatches(self, containerType: MatchContainers, offset: int = 0, numberPast: int = 20,
                      predefinedFilter: MatchType = MatchType.TopTier):
        self.validateNumPastMatches(numberPast, containerType)
        correctUrl = self.getCorrectGetAllMatchesUrl(containerType, predefinedFilter, offset)
        theSoup = self.soupChef.makeSoup(correctUrl)
        matches = self.getMatchesFromSoup(theSoup, containerType)
        if containerType == MatchContainers.past:
            matches = matches[:numberPast]
        return matches

    def getCorrectFactory(self, containerType: MatchContainers) -> AbstractMatchFactory:
        match containerType:
            case MatchContainers.past:
                return self.pastMatchFactory
            case MatchContainers.present:
                return self.currentMatchFactory
            case MatchContainers.future:
                return self.futureMatchFactory
            case MatchContainers.byTeam:
                return self.matchByTeamFactory
            case _:
                raise TypeError("containerType has to be of type MatchContainer")

    def getCorrectGetAllMatchesUrl(self, containerType: MatchContainers, predefinedFilter: MatchType, offset: int):
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

    def validateNumPastMatches(self, numberPast: int, containerType: MatchContainers):
        if MatchContainers.past == containerType and numberPast > 100:
            raise ValueError("Cannot get more than 100 past matches at a time. Please modify the offset if you want "
                             "to go further into the past")

    def getFutureMatchesByDay(self, theSoup: soup.element.Tag, lookForDate) -> [FutureMatch]:
        correctMatchDay = self.getCorrectFutureMatchDay(theSoup, lookForDate)
        return self.getMatchesFromSoup(correctMatchDay, MatchContainers.future)

    def getTodaysMatches(self, theSoup: soup.element.Tag) -> [Match]:
        liveMatches = self.getAllMatches(MatchContainers.present, predefinedFilter=MatchType.Default)
        todayDate = datetime.today().date()
        upcomingMatchesToday = self.getFutureMatchesByDay(theSoup, todayDate)
        return liveMatches + upcomingMatchesToday

    def getCorrectFutureMatchDay(self, theSoup: soup.element.Tag, lookForDate):
        matchDays = theSoup.find_all(class_="upcomingMatchesSection")
        correctMatchDay = None
        for matchDay in matchDays:
            matchDayDate = self.mapToDate(matchDay.div.getText()[-10:])
            if matchDayDate == lookForDate:
                correctMatchDay = matchDay
                break
        if not correctMatchDay:
            raise ValueError("Could not find matches for ", lookForDate)
        return correctMatchDay

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
            theDate = self.mapFromResultDateToDate(theSoup.div.getText())
            if theDate == lookForDate:
                soupsToSearch.append(theSoup)
        matches = []
        for soupToSearch in soupsToSearch:
            matches.append(self.getMatchesFromSoup(soupToSearch, MatchContainers.past))
        return matches

    def getSeriesStats(self, matchLink: str):
        if not matchLink.startswith("https://www.hltv.org"):
            raise ValueError("Please provide a valid game url")
        theSoup = self.soupChef.makeSoup(matchLink)
        series = self.seriesFactory.createSeries(theSoup)
        return series

    def getNews(self):
        url = self.urlBuilder.buildGetNewsUrl()
        theSoup = self.soupChef.makeSoup(url)
        news = []
        newsContainers = theSoup.find_all(class_="newsline article")
        for newsContainer in newsContainers:
            news.append(self.newsFactory.createNews(newsContainer))
        return news

    def mapFromResultDateToDate(self, title):
        dateFromTitle = title[12:]
        dateAsArray = dateFromTitle.split(" ")
        dateAsArray[1] = dateAsArray[1][:2]
        theDateStr = "".join(dateAsArray)
        try:
            return datetime.strptime(theDateStr, "%B %d %Y").date()
        except ValueError:
            raise ValueError("Could not transform from result title to date")

