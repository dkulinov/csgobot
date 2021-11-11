from DiscordBot.InputTeams import InputTeams
from ..Types.Team import HLTVTeams
from ..Exceptions.InvalidTeamException import InvalidTeamException

def mapInputToCorrectHltvTeam(inputTeam: str) -> str:
    if not InputTeams.getIsValid(inputTeam):
        raise InvalidTeamException("This team isn't part of the valid inputs.")

    lowerCaseInputTeam = inputTeam.strip().lower().replace(" ", "-")
    hltvTeamName = lowerCaseInputTeam
    if lowerCaseInputTeam == "navi":
        hltvTeamName = "natus-vincere"
    elif lowerCaseInputTeam in ["cph-flames", "cph flames"]:
        hltvTeamName = "copenhagen-flames"
    elif lowerCaseInputTeam in ["mouz-sports", "mouz sports"]:
        hltvTeamName = "mouz"
    elif lowerCaseInputTeam in ["vp", "virtus pro", "virtus-pro"]:
        hltvTeamName = "virtus.pro"
    elif lowerCaseInputTeam in ["tl"]:
        hltvTeamName = "liquid"
    elif lowerCaseInputTeam == "eg":
        hltvTeamName = "evil-geniuses"
    elif lowerCaseInputTeam == "movistar":
        hltvTeamName = "movistar-riders"
    elif lowerCaseInputTeam == "partynauts":
        hltvTeamName = "party-astronauts"
    elif lowerCaseInputTeam == "bnb":
        hltvTeamName = "bad-news-bears"
    elif lowerCaseInputTeam == "es":
        hltvTeamName = "extra-salt"

    if not HLTVTeams.getIsValid(hltvTeamName):
        raise InvalidTeamException("This team isn't part of the supported HLTV teams")

    return hltvTeamName