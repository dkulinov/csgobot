from bs4 import element

from Commons.Types.News import News


class NewsFactory:
    def __init__(self):
        pass

    def validateContainer(self, container: element.Tag):
        containerClasses: list = container['class']
        try:
            containerClasses.index("newsline")
        except ValueError:
            raise ValueError('Could not create news from this container')

    def createNews(self, container: element.Tag) -> News:
        self.validateContainer(container)
        link = self.getLink(container)
        title = self.getTitle(container)
        return News(link, title)

    def getLink(self, container: element.Tag) -> str:
        return "https://www.hltv.org" + container.get('href')

    def getTitle(self, container: element.Tag) -> str:
        return container.find(class_="newstext").getText()
