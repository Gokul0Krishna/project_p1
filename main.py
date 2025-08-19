from Scraper_tool import Scraper
from Encoder_tool import Encoder
def main():
    scraper=Scraper()
    encoder=Encoder()
    # put a if statement here to run this if and only if db file doesn't exist
    with open('websites.txt','r+') as file:
        for i in file:
            i = i.replace('\n','')
            txt = scraper.scrape(i)
            if len(txt)<1000:
                pass
            chunks = encoder.chunking(text=txt)
            encoder.embedder(chunks=chunks,source_id=i)
        
        
    
if __name__=='__main__':
    main()
