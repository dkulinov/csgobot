from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from Commons.Types.MatchType import MatchType
from Commons.Types.Match import Match
from Commons.Types.Team import HLTVTeams
from Commons.Types.MatchStats import MatchStats
from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Mappers.InputToHtlvTeam import mapInputToCorrectHltvTeam

baseUrl = "https://www.hltv.org/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
}


def getUpcomingMatches(predefinedFilter: MatchType = MatchType.TopTier) -> [Match]:
    url = baseUrl + "matches"
    url += "?predefinedFilter=" if predefinedFilter != MatchType.Default else ""
    url += predefinedFilter.value
    print(url)
    req = Request(url, headers=headers)
    res = urlopen(req)
    html = res.read()

    theSoup = soup(html, "html.parser")
    team1s = theSoup.find_all(class_='team1')
    team2s = theSoup.find_all(class_='team2')
    numMatches = len(team1s)
    for i in range(numMatches):
        print("\nMatch: " + team1s[i].get_text().strip() + " vs " + team2s[i].get_text().strip())

    return [Match()]


def getUpcomingMatchesByTeam(team: str) -> [Match]:
    try:
        validTeam = mapInputToCorrectHltvTeam(team)
    except InvalidTeamException as err:
        return str(err)
    pass


#
# def getPastMatches(predefinedFilter: MatchType, team: str= "None") -> [Match]:
#     return [Match()]
#
# def getCurrentMatches(predefinedFilter: MatchType, team:str = "None") -> [Match]:
#     return [Match()]
#
# def getStats(team1, team2) -> MatchStats:
#     return MatchStats()

getUpcomingMatches()
