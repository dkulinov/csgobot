from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as soup, element

from HLTVScraper.Helpers import UrlBuilder


class SoupChef:
    def __init__(self, urlBuilder: UrlBuilder):
        self.urlBuilder = urlBuilder

    def makeSoup(self, url: str) -> element.Tag:
        headers = self.urlBuilder.getHeaders()
        req = Request(url, headers=headers)
        res = urlopen(req)
        html = res.read()
        return soup(html, "html.parser")
