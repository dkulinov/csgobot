from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

from Commons.Types.Match.MatchByTeam import MatchByTeam
from Commons.Types.Match.CurrentMatch import CurrentMatch
from Commons.Types.Match.FutureMatch import FutureMatch
from Commons.Types.Match.PastMatch import PastMatch
from Commons.Types.MatchType import MatchType
from Commons.Types.SeriesStats import SeriesStats
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchTime import MatchTime
from HLTVScraper.Helpers.Factories.MatchFactories.CurrentMatchFactory import CurrentMatchFactory
from HLTVScraper.Helpers.Factories.MatchFactories.FutureMatchFactory import FutureMatchFactory
from HLTVScraper.Helpers.Factories.MatchFactories.MatchByTeamFactory import MatchByTeamFactory
from HLTVScraper.Helpers.Factories.MatchFactories.PastMatchFactory import PastMatchFactory
from HLTVScraper.Helpers.Factories.NewsFactory import NewsFactory
from HLTVScraper.Helpers.Factories.SeriesFactory import SeriesFactory
from HLTVScraper.Helpers.SoupChef import SoupChef
from HLTVScraper.Helpers.UrlBuilder import URLBuilder
from HLTVScraper.scraper import Scraper

# url = "https://www.hltv.org/matches/2353955/astralis-vs-fnatic-funspark-ulti-2021-finals"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
# }
#
# req = Request(url, headers=headers)
# res = urlopen(req)
# html = res.read()
# theSoup = soup(html, "html.parser")
# a=theSoup.find('a')
# print(type(theSoup))
# print(a)


urlBuilder = URLBuilder()
soupChef = SoupChef(urlBuilder)
pastMatchFactory = PastMatchFactory()
currentMatchFactory = CurrentMatchFactory()
futureMatchFactory = FutureMatchFactory()
seriesFactory = SeriesFactory()
matchByTeamFactory = MatchByTeamFactory()
newsFactory = NewsFactory()

scraper = Scraper(urlBuilder, soupChef, pastMatchFactory, currentMatchFactory, futureMatchFactory,
                  seriesFactory, matchByTeamFactory, newsFactory)

# NEWS:
# news = scraper.getNews()
# for theNews in news:
#     print("{}. For more go to: {}.".format(theNews.title, theNews.link))

# GET ALL MATCHES (past)
# pastMatches: [PastMatch] = scraper.getAllMatches(MatchContainers.past, numberPast=10)
# for pastMatch in pastMatches:
#     print("{} {} {} VS {} {} {}. MORE: {}".format(pastMatch.team1, pastMatch.team1Logo, pastMatch.team1Score, pastMatch.team2Score, pastMatch.team2, pastMatch.team2Logo, pastMatch.link))

# TODO: test this
# GET ALL MATCHES (live)
# liveMatches: [CurrentMatch] = scraper.getAllMatches(MatchContainers.present, predefinedFilter=MatchType.Default)
# for liveMatch in liveMatches:
#     print("BO{}: {} {} {} {} VS {} {} {} {}. MORE: {}".format(liveMatch.bestOf, liveMatch.team1, liveMatch.team1Logo, liveMatch.team1CuMapScore, liveMatch.team1MapsWon, liveMatch.team2, liveMatch.team2Logo, liveMatch.team2CuMapScore, liveMatch.team2MapsWon, liveMatch.link))

# GET ALL MATCHES (future)
# futureMatches: [FutureMatch] = scraper.getAllMatches(MatchContainers.future, predefinedFilter=MatchType.TopTier)
# for futureMatch in futureMatches:
#     if futureMatch.emptyMatchDescription:
#         print("BO{} at {}: {}. MORE: {}".format(futureMatch.bestOf, futureMatch.epochTime, futureMatch.emptyMatchDescription, futureMatch.link))
#     else:
#         print("BO{} at {}: {} {} VS {} {}. MORE: {}".format(futureMatch.bestOf, futureMatch.epochTime, futureMatch.team1, futureMatch.team1Logo, futureMatch.team2, futureMatch.team2Logo, futureMatch.link))


# GET MATCHES BY TEAM (future)
# futureMatchesByTeam: [MatchByTeam] = scraper.getMatchesByTeam("navi")
# for futureMatchByTeam in futureMatchesByTeam:
#     print("{}. {} {} {} vs {} {} {}. MORE: {}".format(futureMatchByTeam.epochTime, futureMatchByTeam.team1, futureMatchByTeam.team1Logo, futureMatchByTeam.team1Score, futureMatchByTeam.team2Score, futureMatchByTeam.team2Logo, futureMatchByTeam.team2, futureMatchByTeam.link))

# GET MATCHES BY TEAM (past)
# pastMatchesByTeam: [MatchByTeam] = scraper.getMatchesByTeam("navi", MatchTime.past)
# for pastMatchByTeam in pastMatchesByTeam:
#     print("{}. {} {} {} vs {} {} {}. MORE: {}".format(pastMatchByTeam.epochTime, pastMatchByTeam.team1, pastMatchByTeam.team1Logo, pastMatchByTeam.team1Score, pastMatchByTeam.team2Score, pastMatchByTeam.team2Logo, pastMatchByTeam.team2, pastMatchByTeam.link))

# GET SERIES STATS
# seriesStats: SeriesStats = scraper.getSeriesStats("https://www.hltv.org/matches/2353605/gambit-vs-natus-vincere-blast-premier-world-final-2021")
# print("{} {} vs {} {}".format(seriesStats.team1Name, seriesStats.team1MapsWon, seriesStats.team2Name, seriesStats.team2MapsWon))
# for map in seriesStats.matches:
#     print(map.mapName)
#     print(map.team1Score, map.team2Score)
#     for team1Stat in map.team1Stats:
#         print(team1Stat.player, team1Stat.kill_death, team1Stat.plus_minus, team1Stat.avg_damage_per_round, team1Stat.kill_assist_survive_traded, team1Stat.rating)
#     for team2Stat in map.team2Stats:
#         print(team2Stat.player, team2Stat.kill_death, team2Stat.plus_minus, team2Stat.avg_damage_per_round,
#               team2Stat.kill_assist_survive_traded, team2Stat.rating)

# GET MATCHES BY DAY (past)
# matchesByDay: [PastMatch] = scraper.getMatchesByDay("01/24/2022")
# for matchByDay in matchesByDay:
#     print("{} {} {} VS {} {} {}. MORE: {}".format(matchByDay.team1, matchByDay.team1Logo, matchByDay.team1Score, matchByDay.team2Score, matchByDay.team2, matchByDay.team2Logo, matchByDay.link))

# GET MATCHES BY DAY (current)
# matchesByDay: [CurrentMatch] = scraper.getMatchesByDay("01/25/2022")
# for matchByDay in matchesByDay:
#     print("{} {} {} VS {} {} {}. MORE: {}".format(matchByDay.team1, matchByDay.team1Logo, matchByDay.team1Score, matchByDay.team2Score, matchByDay.team2, matchByDay.team2Logo, matchByDay.link))


# GET MATCHES BY DAY (future)
matchesByDay: [FutureMatch] = scraper.getMatchesByDay("01/26/2022")
for futureMatch in matchesByDay:
    if futureMatch.emptyMatchDescription:
        print("BO{} at {}: {}. MORE: {}".format(futureMatch.bestOf, futureMatch.epochTime, futureMatch.emptyMatchDescription, futureMatch.link))
    else:
        print("BO{} at {}: {} {} VS {} {}. MORE: {}".format(futureMatch.bestOf, futureMatch.epochTime, futureMatch.team1, futureMatch.team1Logo, futureMatch.team2, futureMatch.team2Logo, futureMatch.link))


# print(len(matchesByDay))