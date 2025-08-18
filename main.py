from Scraper_tool import Scraper
def main():
    scraper=Scraper()
    # put a if statement here to run this if and only if db file doesn't exist
    with open('websites.txt','r+') as file:
        for i in file:
            # print(i)
            i = i.replace('\n','')
            txt = scraper.scrape(i)
            # print(len(txt.split()))
        
            
if __name__=='__main__':
    main()
