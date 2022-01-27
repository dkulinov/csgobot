# from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as soup, element

from HLTVScraper.Helpers import UrlBuilder

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class SoupChef:
    def __init__(self, urlBuilder: UrlBuilder):
        self.urlBuilder = urlBuilder

    def makeSoup(self, url: str) -> element.Tag:
        # headers = self.urlBuilder.getHeaders()
        # req = Request(url, headers=headers)
        # res = urlopen(req, timeout=20)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        html = driver.page_source
        return soup(html, "html.parser")
