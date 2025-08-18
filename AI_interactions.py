import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import LLM,Agent,Task,Crew

class Credentials():
    def __init__(self):
        'loads all credentials and model'

        load_dotenv(dotenv_path=Path('.env'))
        self.llm_api_key = os.getenv("deepseekkey")
        self.model = LLM(model="deepseek/deepseek-chat-v3-0324:free",
                              api_key=self.llm_api_key,
                              base_url="https://openrouter.ai/api/v1"
                        )

class Datagatherer(Credentials):
    'Fetches given no. of website links on given topic'
    def __init__(self, topic:str, n:int):
        super().__init__()
        self.agent = Agent(
            role = "Data gatherer",
            goal = "get website links for the given topic",
            backstory ="you are master at fetching the information from the web",
            llm=self.model
            )
        
        self.task = Task(
            description = f"fecth {n} websites links of companies that are {topic}",
            expected_output = "list of website links",
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


class Scrapper(Credentials):
    def __init__(self):
        super().__init__()
        self.agent = Agent(
                role = "Information Gatherer ",
                goal = "Retrive all posible i",
                backstory ="you are master at fetching the information from the web",
                llm=self.model
                )
            
        self.task = Task(
            description = f"fecth {n} websites links of companies that are {topic}",
            expected_output = "list of website links",
            agent = self.agent
            )

if __name__=="__main__":
    obj=Datagatherer(n=5,topic="llm")
    "i"