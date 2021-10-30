from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from Commons.Types.MatchType import MatchType
from Commons.Types.Match import Match
from Commons.Types.Match import Team
from Commons.Types.MatchStats import MatchStats
baseUrl = "https://www.hltv.org/"


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
req = Request(baseUrl + "matches", headers=headers)
res = urlopen(req)
html = res.read()

soup = soup(html, "html.parser")
matches = soup.find_all(class_='matchTeams')
for match in matches:
    print("\nMatch: ", match)

def getUpcomingMatches(predefinedFilter: MatchType, team: str = "None") -> [Match]:
    return [Match()]

def getPastMatches(predefinedFilter: MatchType, team: str= "None") -> [Match]:
    return [Match()]

def getCurrentMatches(predefinedFilter: MatchType, team:str = "None") -> [Match]:
    return [Match()]

def getStats(team1, team2) -> MatchStats:
    return MatchStats()