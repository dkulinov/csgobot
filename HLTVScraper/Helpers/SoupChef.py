from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as soup

from HLTVScraper.Helpers import UrlBuilder


class SoupChef:
    def __init(self, urlBuilder: UrlBuilder):
        self.urlBuilder = urlBuilder

    def makeSoup(self, url: str):
        headers = self.urlBuilder.getHeaders()
        req = Request(url, headers=headers)
        res = urlopen(req)
        html = res.read()
        return soup(html, "html.parser")
