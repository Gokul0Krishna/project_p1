import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

lit=[
    'https://www.gov.uk/government/statistics/statistics-on-international-development-final-uk-aid-spend-2022/statistics-on-international-development-final-uk-aid-spend-2022',
    'https://www.iom.int/funding-and-donors/united-kingdom',
    'https://publications.parliament.uk/pa/cm201314/cmselect/cmintdev/349/349vw07.htm',
    'https://www.oecd.org/en/publications/development-co-operation-profiles_04b376d7-en/united-kingdom_052bbc63-en.html',
]

for i in lit:
    response=requests.get(i)
    soup = BeautifulSoup(response.text,'html.parser')
    txt = soup.get_text()
    txt = re.sub(r"\s+", " ", txt)
    txt = re.sub(r"[^\x20-\x7E\n\t]", "", txt)
    txt=(txt.encode("utf-8", errors="ignore")).decode()

