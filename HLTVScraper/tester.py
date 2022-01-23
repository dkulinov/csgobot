from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

from Commons.Types.Match.PastMatch import PastMatch
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
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
pastMatches: PastMatch = scraper.getAllMatches(MatchContainers.past, numberPast=30)
for pastMatch in pastMatches:
    print("Logo {} of {} SCORE {} VS SCORE {} {} Logo {}. MORE: {}".format(pastMatch.team1, pastMatches.team1Logo, pastMatch.team1Score, pastMatch.team2, pastMatches.team2Logo, pastMatch.team2Score, pastMatch.link))
