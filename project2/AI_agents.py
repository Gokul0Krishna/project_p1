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

class ReturnretrivalTool(BaseTool):
    name: str = "Return information retrival Tool"
    description: str = "retrives the return policy data"
    def _run(self):
        return_policy = """
                        You can return products within 30 days of purchase with the original receipt.
                        Refunds will be issued to the original payment method.
                        """
        return return_policy
    
class InventoryretrivalTool(BaseTool):
    name: str = "Inventory information retrival Tool"
    description: str = "retrives the Inventory data"
    def _run(self):
        inventory = {
                        "nike shoes": 15,
                        "adidas hoodie": 0,
                        "puma shorts": 8
                    }
        return inventory



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
    
        inventory_tool = InventoryretrivalTool()
        return_policy_tool = ReturnretrivalTool()

        self.support_agent = Agent(
            role="Customer Support Assistant",
            goal=(
                "Provide accurate and helpful answers to customer questions about "
                "orders, product availability, and return policies. "
                "Use the tools provided whenever needed: "
                "- Use the Inventory Retrieval Tool for questions about stock levels, product details, or availability. "
                "- Use the Return Policy Retrieval Tool for questions about return rules, timelines, or procedures. "
                "If both topics are involved, combine information from both tools into one clear response."
            ),
            backstory="You are a JD Sports support agent who always relies on internal tools for accurate information.",
            tools=[inventory_tool, return_policy_tool],
            llm=self.model,
            verbose=True
        )

        # Task definition
        self.task = Task(
            description=(
                "Answer the customer query: {query}. "
                "Use the Inventory Retrieval Tool for inventory-related questions "
                "and the Return Policy Retrieval Tool for return-related questions. "
                "If both apply, use both tools and provide a single, concise answer."
            ),
            agent=self.support_agent,
            expected_output="A clear and helpful natural language response that answers the customer's query using the correct tools."
        )


    
    def rn(self,query:str):
        crew = Crew(agents=[self.support_agent], tasks=[self.task])
        return crew.kickoff(inputs={"query": query})      

if __name__=='__main__':
    obj=AI()
    print(obj.rn(query= "Do you have Adidas Hoodie in stock?"))
                