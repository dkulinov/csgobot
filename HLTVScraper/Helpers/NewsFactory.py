from bs4 import BeautifulSoup as soup

from Commons.Types import News


class NewsFactory:
    def __init__(self):
        pass

    def validateContainer(self, container: soup.element.Tag):
        if container['class'] != "newsline article":
            raise ValueError('Could not create news from this container')

    def createNews(self, container: soup.element.Tag) -> News:
        self.validateContainer(container)
        link = self.getLink(container)
        title = self.getTitle(container)
        return News(link, title)

    def getLink(self, container: soup.element.Tag) -> str:
        return "https://www.hltv.org" + container.get('href')

    def getTitle(self, container: soup.element.Tag) -> str:
        return container.find(class_="newstext").getText()
