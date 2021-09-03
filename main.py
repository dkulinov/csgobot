from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

baseUrl = "https://www.hltv.org/matches"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
req = Request(baseUrl, headers=headers)
res = urlopen(req)
html = res.read()

soup = soup(html, "html.parser")
matches = soup.find_all(class_='matchTeams')
for match in matches:
    print("\nMatch: ", match)

