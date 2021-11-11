from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from Commons.Types.MatchType import MatchType
from Commons.Types.Match import Match
from Commons.Types.Team import HLTVTeams
from Commons.Types.MatchStats import MatchStats

baseUrl = "https://www.hltv.org/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
}


def getUpcomingMatches(predefinedFilter: MatchType, team: Team = None) -> [Match]:
    if team is None:
        req = Request(baseUrl + "matches", headers=headers)
    else:
        # find match by team
    res = urlopen(req)
    html = res.read()

    theSoup = soup(html, "html.parser")
    matches = theSoup.find_all(class_='matchTeams')
    for match in matches:
        print("\nMatch: ", match)

    return [Match()]
#
# def getPastMatches(predefinedFilter: MatchType, team: str= "None") -> [Match]:
#     return [Match()]
#
# def getCurrentMatches(predefinedFilter: MatchType, team:str = "None") -> [Match]:
#     return [Match()]
#
# def getStats(team1, team2) -> MatchStats:
#     return MatchStats()
