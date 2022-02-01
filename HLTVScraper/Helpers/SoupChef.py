# from urllib.request import Request, urlopen
from time import sleep

from bs4 import BeautifulSoup as soup, element

from HLTVScraper.Helpers import UrlBuilder

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class SoupChef:
    def __init__(self, urlBuilder: UrlBuilder):
        self.urlBuilder = urlBuilder

    def makeSoup(self, url: str, tz: str = "America/Phoenix") -> element.Tag:
        # headers = self.urlBuilder.getHeaders()
        # req = Request(url, headers=headers)
        # res = urlopen(req, timeout=20)
        # TODO: check if this can be used https://stackoverflow.com/questions/59665773/why-render-requests-html-doesnt-scrape-dynamic-content
        driver = webdriver.Chrome(ChromeDriverManager().install())
        tz_params = {'timezoneId': tz}
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
        driver.get(url)
        if url == "https://www.hltv.org/matches":
            sleep(1)
        html = driver.page_source
        return soup(html, "html.parser")
