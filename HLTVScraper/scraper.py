from datetime import datetime
from datetime import timedelta
from bs4 import element
from Commons.Types.Match import PastMatch, FutureMatch
from Commons.Types.Match.Match import Match
from Commons.Types.Match.MatchByTeam import MatchByTeam
from Commons.Types.MatchType import MatchType
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchTime import MatchTime
from HLTVScraper.Helpers import UrlBuilder, SoupChef
from HLTVScraper.Helpers.Factories.MatchFactories.CurrentMatchFactory import CurrentMatchFactory
from HLTVScraper.Helpers.Factories.MatchFactories.FutureMatchFactory import FutureMatchFactory
from HLTVScraper.Helpers.Factories.MatchFactories.MatchByTeamFactory import MatchByTeamFactory
from HLTVScraper.Helpers.Factories.MatchFactories.MatchFactory import AbstractMatchFactory
from HLTVScraper.Helpers.Factories.MatchFactories.PastMatchFactory import PastMatchFactory
from HLTVScraper.Helpers.Factories.NewsFactory import NewsFactory
from HLTVScraper.Helpers.Factories.SeriesFactory import SeriesFactory
from HLTVScraper.Helpers.Factories.TopTeamFactory import TopTeamFactory


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
            topTeamFactory: TopTeamFactory,
    ):
        self.urlBuilder = urlBuilder
        self.pastMatchFactory = pastMatchFactory
        self.currentMatchFactory = currentMatchFactory
        self.futureMatchFactory = futureMatchFactory
        self.matchByTeamFactory = matchByTeamFactory
        self.seriesFactory = seriesFactory
        self.soupChef = soupChef
        self.newsFactory = newsFactory
        self.topTeamFactory = topTeamFactory

    def _getMatchesFromSoup(self, theSoup: element.Tag, containerType: MatchContainers):
        matches = []
        correctFactory = self._getCorrectFactory(containerType)
        matchContainers = theSoup.find_all(class_=containerType.value)
        for matchContainer in matchContainers:
            matches.append(correctFactory.createMatch(matchContainer))
        return matches

    def getMatchesByTeam(self, team: str, timeFrame: MatchTime = MatchTime.future) -> [MatchByTeam]:
        url = self.urlBuilder.buildGetMatchesByTeamUrl(team)
        theSoup = self.soupChef.makeSoup(url)
        emptyFutureMatches = theSoup.find(id='matchesBox').find(class_='empty-state')
        if timeFrame == MatchTime.future and emptyFutureMatches:
            return []
        if not emptyFutureMatches:
            theSoup = theSoup.find_all(class_="match-table")[timeFrame.value]
        else:
            theSoup = theSoup.find(class_="match-table")
        return self._getMatchesFromSoup(theSoup, MatchContainers.byTeam)


    # https://stackoverflow.com/questions/3467114/how-are-cookies-passed-in-the-http-protocol#:~:text=Cookies%20are%20passed%20as%20HTTP,(server%20%2D%3E%20client).
    def getMatchesByDay(self, theDate: str, tz: str) -> [Match]:
        lookForDate = self._mapToDate(theDate, "%m/%d/%Y")
        todayDate = datetime.today().date()
        self._validateDateNotMoreThanWeekBefore(lookForDate)
        url = self._getMatchesByDayUrl(lookForDate, todayDate)
        theSoup = self.soupChef.makeSoup(url, tz)
        matches = []
        if lookForDate < todayDate:
            matches = self._getPastMatchesByDay(lookForDate, tz)
        elif lookForDate == todayDate:
            matches = self._getTodaysMatches(theSoup, tz)
        elif lookForDate > todayDate:
            matches = self._getFutureMatchesByDay(theSoup, lookForDate)
        return matches

    def getAllMatches(self, containerType: MatchContainers, offset: int = 0, numberPast: int = 25,
                      predefinedFilter: MatchType = MatchType.Default):
        self._validatePastMatchParams(numberPast, offset, containerType)
        lookingForPast = containerType == MatchContainers.past
        correctUrl = self._getCorrectGetAllMatchesUrl(containerType, predefinedFilter, offset)
        theSoup = self.soupChef.makeSoup(correctUrl)
        if lookingForPast:
            theSoup = theSoup.find(class_="allres")
        matches = self._getMatchesFromSoup(theSoup, containerType)
        if lookingForPast:
            matches = matches[:numberPast]
        return matches

    def _getCorrectFactory(self, containerType: MatchContainers) -> AbstractMatchFactory:
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

    def _getCorrectGetAllMatchesUrl(self, containerType: MatchContainers, predefinedFilter: MatchType, offset: int):
        match containerType:
            case MatchContainers.past:
                return self.urlBuilder.buildGetPastMatches(offset)
            case MatchContainers.present:
                return self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
            case MatchContainers.future:
                return self.urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter)
            case _:
                raise TypeError("containerType has to be of type MatchContainer")

    def _getMatchesByDayUrl(self, lookForDate, todayDate):
        if lookForDate < todayDate:
            return self.urlBuilder.buildGetPastMatches()
        elif lookForDate == todayDate:
            return self.urlBuilder.buildGetUpcomingMatchesUrl()
        elif lookForDate > todayDate:
            return self.urlBuilder.buildGetUpcomingMatchesUrl()

    def _mapToDate(self, theDate: str, dateFormat: str):
        try:
            return datetime.strptime(theDate, dateFormat).date()
        except ValueError:
            raise ValueError("Date has to be in the mm/dd/yyyy format.")

    def _validateDateNotMoreThanWeekBefore(self, lookForDate):
        weekBeforeToday = datetime.today().date() - timedelta(days=7)
        if lookForDate < weekBeforeToday:
            raise ValueError("Cannot look up matches more than a week before today.")

    def _validatePastMatchParams(self, numberPast: int, offset: int, containerType: MatchContainers):
        if MatchContainers.past == containerType and numberPast < 1:
            raise ValueError("Number of matches has to be positive")
        if MatchContainers.past == containerType and numberPast > 25:
            raise ValueError("Cannot get more than 25 past matches at a time. Please modify the offset if you want "
                             "to go further into the past")
        if MatchContainers.past == containerType and offset < 0:
            raise ValueError("Offset can't be a negative number")

    def _getFutureMatchesByDay(self, theSoup: element.Tag, lookForDate) -> [FutureMatch]:
        correctMatchDay = self._getCorrectFutureMatchDay(theSoup, lookForDate)
        return self._getMatchesFromSoup(correctMatchDay, MatchContainers.future)

    def _getTodaysMatches(self, theSoup: element.Tag, tz: str) -> [Match]:
        todayDate = datetime.today().date()
        previousMatches = self._getPastMatchesByDay(todayDate, tz)
        liveMatches = self.getAllMatches(MatchContainers.present, predefinedFilter=MatchType.Default)
        try:
            upcomingMatchesToday = self._getFutureMatchesByDay(theSoup, todayDate)
        except ValueError:
            upcomingMatchesToday = []
        return liveMatches + upcomingMatchesToday + previousMatches

    def _getCorrectFutureMatchDay(self, theSoup: element.Tag, lookForDate: datetime):
        matchDays = theSoup.find_all(class_="upcomingMatchesSection")
        correctMatchDay = None
        for matchDay in matchDays:
            matchDayDate = self._mapToDate(matchDay.find_next().getText()[-10:], "%Y-%m-%d")
            if matchDayDate == lookForDate:
                correctMatchDay = matchDay
                break
        if correctMatchDay is None:
            raise ValueError(f"There are no matches on {lookForDate.strftime('%m-%d-%Y')}")
        return correctMatchDay

    def _getPastMatchesByDay(self, lookForDate, tz: str) -> [PastMatch]:
        maxDays = 8
        daysSearched = 0
        soups = []
        offset = 0
        while daysSearched < maxDays:
            url = self.urlBuilder.buildGetPastMatches(offset)
            soup = self.soupChef.makeSoup(url, tz).find(class_="allres")
            dayResultContainers = soup.find_all(class_="results-sublist")
            soups.extend(dayResultContainers)
            daysSearched += len(dayResultContainers)
            offset += 100
            lastDayTitle = dayResultContainers[-1].find_next().getText()
            while daysSearched == maxDays:
                url = self.urlBuilder.buildGetPastMatches(offset)
                soup = self.soupChef.makeSoup(url, tz)
                dayResultContainers = soup.find_all(class_="results-sublist")
                soups.append(dayResultContainers[0])
                offset += 100
                newTitle = dayResultContainers[-1].find_next().getText()
                if newTitle != lastDayTitle:
                    daysSearched += 1
        soupsToSearch = []
        for theSoup in soups:
            theDate = self._mapFromResultDateToDate(theSoup.find_next().getText())
            if theDate == lookForDate:
                soupsToSearch.append(theSoup)
        matches = []
        for soupToSearch in soupsToSearch:
            matches.extend(self._getMatchesFromSoup(soupToSearch, MatchContainers.past))
        return matches

    def getSeriesStats(self, matchLink: str):
        if not matchLink.startswith("https://www.hltv.org/matches/"):
            raise ValueError("Please provide a valid game url")
        theSoup = self.soupChef.makeSoup(matchLink)
        series = self.seriesFactory.createSeries(theSoup)
        return series

    def getNews(self):
        url = self.urlBuilder.buildGetNewsUrl()
        theSoup = self.soupChef.makeSoupFast(url)
        news = []
        newsContainers = theSoup.find_all(class_="newsline article")
        for newsContainer in newsContainers:
            news.append(self.newsFactory.createNews(newsContainer))
        return news

    def _mapFromResultDateToDate(self, title):
        dateFromTitle = title[12:]
        dateAsArray = dateFromTitle.split(" ")
        dateAsArray[1] = "".join(list(filter(lambda ch: ch.isnumeric(), dateAsArray[1])))
        theDateStr = dateAsArray[0] + " " + dateAsArray[1] + " " + dateAsArray[2]
        try:
            return datetime.strptime(theDateStr, "%B %d %Y").date()
        except ValueError:
            raise ValueError("Could not transform from result title to date")

    # Team rankings
    def getTopTeams(self):
        url = self.urlBuilder.buildGetTopTeamsUrl()
        theSoup = self.soupChef.makeSoupFast(url)
        topTeams = []
        topTeamContainers = theSoup.find_all(class_="ranked-team")
        for topTeamContainer in topTeamContainers:
            topTeams.append(self.topTeamFactory.createTopTeam(topTeamContainer))
        return topTeams
