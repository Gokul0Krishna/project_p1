import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew ,LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Mock database

return_policy = """
You can return products within 30 days of purchase with the original receipt.
Refunds will be issued to the original payment method.
"""

inventory = {
    "nike shoes": 15,
    "adidas hoodie": 0,
    "puma shorts": 8
}

class InformationretrivalTool(BaseTool):
    name: str = "Information retrival Tool"
    description: str = "retrives the stored data"
    def _run(self):
        return_policy = """
                        You can return products within 30 days of purchase with the original receipt.
                        Refunds will be issued to the original payment method.
                        """

        inventory = {
                    "nike shoes": 15,
                    "adidas hoodie": 0,
                    "puma shorts": 8
                    }
        return return_policy,inventory


class AI():
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
            api_version = self.llm_version
        )
    
        tool=InformationretrivalTool()
        self.support_agent = Agent(
                                role="Customer Support Assistant",
                                goal="Answer customers's querries about orders, returns, and inventory using provided tool",
                                backstory="You are a JD Sports support agent.",
                                tools=[tool],
                                llm=self.model,
                                verbose=True
                            )

        # Task definition
        self.task = Task(
                            description="Answer the customer query: {query} about returns or inventory using the given tool",
                            agent=self.support_agent,
                            expected_output="A helpful and concise natural language response to the customer's query"
                        )

    
    def rn(self,query:str):
        crew = Crew(agents=[self.support_agent], tasks=[self.task])
        return crew.kickoff(inputs={"query": query})      

if __name__=='__main__':
    obj=AI()
    print(obj.rn(query= "Do you have Adidas Hoodie in stock?"))
                