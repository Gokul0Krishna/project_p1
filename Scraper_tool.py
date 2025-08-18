# import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import cloudscraper

class Scraper():
    def scrape(self,url:str)->str:
        'scrapes the given url and provids information'
        scraper = cloudscraper.create_scraper()
        headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                                "AppleWebKit/537.36 (KHTML, like Gecko)"
                                "Chrome/114.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://www.iom.int/",
                    }
        response = scraper.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'html.parser')
        txt = soup.get_text()
        txt = re.sub(r"\s+", " ", txt)
        txt = re.sub(r"[^\x20-\x7E\n\t]", "", txt)
        txt = (txt.encode("utf-8", errors="ignore")).decode()
        return txt

# scraper = cloudscraper.create_scraper()
# response=scraper.get('https://www.iom.int/funding-and-donors/united-kingdom')
# soup = BeautifulSoup(response.text,'html.parser')
# print(soup)

