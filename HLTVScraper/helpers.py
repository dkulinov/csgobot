
class urlBuilder:

    def __init__(self):
        baseUrl = "https://www.hltv.org/"

    def buildGetUpcomingMatchesUrl(team: str) -> str:
        if team is None:
            path = "/matches"
        else:
            path = "/team/10786/river-plate#tab-matchesBox"

        return baseUrl + path