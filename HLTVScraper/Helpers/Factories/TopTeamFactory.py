from Commons.Types.TopTeam import TopTeam
from bs4 import element


class TopTeamFactory:
    def __init__(self):
        pass

    def validateContainer(self, container: element.Tag):
        if "ranked-team" not in container['class']:
            raise TypeError("Can't create TopTeam from given container")

    def createTopTeam(self, container: element.Tag):
        self.validateContainer(container)
        teamName = self.getTeamName(container)
        teamLogo = self.getTeamLogo(container)
        points = self.getPoints(container)
        change = self.getChange(container)
        link = self.getLink(container)
        return TopTeam(teamName, teamLogo, points, change, link)

    def getTeamName(self, container: element.Tag) -> str:
        return container.find(class_="name").getText()

    def getTeamLogo(self, container: element.Tag) -> str:
        return container.find(class_="team-logo").img.get("src")

    def getPoints(self, container: element.Tag) -> str:
        return container.find(class_="points").getText()

    def getChange(self, container: element.Tag) -> str:
        return container.find(class_="change").getText()

    def getLink(self, container: element.Tag)-> str:
        return "https://hltv.org" + container.find(class_="more").a.get('href')
