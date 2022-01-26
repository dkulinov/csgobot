from Commons.Mappers.InputToHtlvTeam import mapInputToCorrectHltvTeam
from Commons.Types.MatchType import MatchType
from Commons.Types.Team import HLTVTeams


class URLBuilder:

    def __init__(self):
        self.baseUrl = "https://www.hltv.org"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
            # TODO: check if cookie can be set for timezone
            # "Set-Cookie": "hltvTimeZone=America/Phoenix"
        }

    def buildGetUpcomingMatchesUrl(self, predefinedFilter: MatchType = MatchType.Default) -> str:
        url = self.baseUrl + '/matches'
        url += "?predefinedFilter=" if predefinedFilter != MatchType.Default else ""
        url += predefinedFilter.value
        return url

    def buildGetMatchesByTeamUrl(self, team: str) -> str:
        normalizedTeamName = mapInputToCorrectHltvTeam(team)
        teamId = HLTVTeams().getTeamId(normalizedTeamName)
        return self.baseUrl + "/team/" + str(teamId) + "/" + normalizedTeamName

    def buildGetPastMatches(self, offset: int = 0) -> str:
        return self.baseUrl + '/results?offset=' + str(offset)

    def buildGetNewsUrl(self):
        return self.baseUrl

    def buildGetTopTeamsUrl(self):
        return self.baseUrl + "/ranking/teams"

    def getHeaders(self):
        return self.headers
