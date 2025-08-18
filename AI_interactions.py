import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import LLM,Agent,Task,Crew

class Credentials():
    def __init__(self):
        'loads all credentials and model'
        load_dotenv(dotenv_path=Path('.env'))
        
        self.llm_api_key = os.getenv('openai.api_key')
        self.llm_base_url = os.getenv('openai.api_base')
        self.llm_version = os.getenv('openai.api_version')

        self.model = LLM(
            model = 'azure/gpt-4o',
            api_base = self.llm_base_url,
            api_key = self.llm_api_key,
            api_version = self.llm_version,
        )



class Scraper(Credentials):
    'scrapes infromation from a given websitle link'
    '''Unfortunately, I cannot directly scrape information from websites or access live internet data at this moment. However, if you     │
│   provide me the content or structure of the web page, I can help format it into JSON or assist with specific details. Alternatively, you can use  │
│   scraping tools like Python's BeautifulSoup or Scrapy to extract the information on your behalf.'''
    'plan scrapped.'
    def __init__(self,):
        super().__init__()
        self.agent = Agent(
            role = "Web scraper",
            goal = "get all infomation from the website",
            backstory ="you are master at scaping information from the web",
            llm=self.model
            )
        
        self.task = Task(
            description = f"from webstie {self.website} scrape infromation in the format in the format on who,how much and to whome",
            expected_output = "json format",
            agent = self.agent
            )
               
    def run(self):
        crew=Crew(
            agents = [self.agent],
            tasks = [self.task],
            verbose = True
            )
        
        result = crew.kickoff()
        print(result)

if __name__=="__main__":
    obj=Scraper()
    obj.run()