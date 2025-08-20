import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew ,LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from typing import Type
from Encoder_tool import Encoder
from Scraper_tool import Scraper 
import re
# from rank_bm25 import BM25Okapi



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

class Retriever(Credentials):
    def __init__(self):
        super().__init__()
        self.embedding = AzureOpenAIEmbeddings( azure_deployment = "embedding-ada",
                                                openai_api_version = "2023-05-15",
                                                api_key = self.llm_api_key,
                                                azure_endpoint = self.llm_base_url
                                                )   
    
        self.vectorstore = Chroma(
                                collection_name = "donors",
                                persist_directory = "chroma_store",  
                                embedding_function = self.embedding
                                )
    def retrieve(self,query:str,top_k=3):
        return self.vectorstore.similarity_search(query, k=top_k)

class RagretrieverInput(BaseModel):
    """Input schema for HybridRetriever."""
    query: str = Field(..., description="The user query to search for relevant documents.")

# --- Tool definition ---
class RagretrieverTool(BaseTool):
    name: str = "Retriever"
    description: str = "Fetches relevant documents from the vector database to support reasoning."
    args_schema: Type[BaseModel] = RagretrieverInput

    def _run(self,query:str,**kwargs)->str:
        """Run retrieval with user query."""
        cred=Credentials()
        embedding = AzureOpenAIEmbeddings( azure_deployment = "embedding-ada",
                                                openai_api_version = "2023-05-15",
                                                api_key = cred.llm_api_key,
                                                azure_endpoint = cred.llm_base_url
                                                )   
    
        vectorstore = Chroma(
                                collection_name = "donors",
                                persist_directory = "chroma_store",  
                                embedding_function = embedding
                                )
        print(f"[RetrieverTool] Running retrieval for query: {query}")
        docs=vectorstore.similarity_search(query, k=3)
        print(f"[RetrieverTool] Found {len(docs)} docs")
        return "\n".join([d.page_content for d in docs]) if docs else "No documents found."


class Websitesaverinput(BaseModel):
    """Input schema for Websitesaver."""
    query: str = Field(..., description="url of a website")

# --- Tool definition ---
class WebsitesaverTool(BaseTool):
    name: str = "Website saver tool"
    description: str = "Stores the given data"
    args_schema: Type[BaseModel] = Websitesaverinput

    def _run(self,website:str,**kwargs):
        """saves the given website."""
        encoder=Encoder()
        scraper=Scraper()
        print(website)
        match = re.search(r"https?://[^\s]+", website)
        if match:
            url = match.group(0)
            print(url)
            if encoder.checking(website=url):
                with open('websites.txt','a+') as file:
                    file.write(f"\n{url}")
                txt = scraper.scrape(url)
                chunks = encoder.chunking(text=txt)
                encoder.embedder(chunks=chunks,source_id=website)
                print('website saved')
                return 'website saved'
            return 'website already exists'
        return 'no website was given'        

class Myagent(Retriever):
    def __init__(self):
        super().__init__()

        self.ragretriever_tool = RagretrieverTool()

        self.websitesaver_tool = WebsitesaverTool()
        
        self.decider = Agent(
                                role="Decider",
                                goal="Judge if the user input is a query or an instruction to save data.",
                                backstory="Acts like a traffic controller. Looks at the input and decides if it's a question to answer or an instruction to store.",
                                llm=self.model,
                                verbose=True
                            )

        self.decision_task = Task(
                                description=(
                                    "Look at the user input: {query}. "
                                    "Decide ONE path:\n"
                                    "- If it's a question (who, what, where, why, how, etc.) → output 'Query'.\n"
                                    "- If it's an instruction to save or store something (like 'save this website', 'add new website') → output 'Save'.\n"
                                    "Answer ONLY with 'Query' or 'Save'."
                                ),
                                expected_output="Either 'Query' or 'Save'.",
                                agent=self.decider
                                )


        self.reasoning_agent = Agent(
                                role="Reasoner",
                                goal="Answer user queries using retrieved context",
                                backstory="An expert at analyzing and summarizing knowledge from documents.",
                                llm=self.model,   # or another LLM
                                tools=[self.ragretriever_tool],  # give it the retriever tool
                                verbose=True
                                )      

        self.reasoning_task = Task(
                                description="Answer the user query: {query}. Use the retriever tool first to gather context, then reason over it.",
                                expected_output="A clear, helpful answer to the query.",
                                agent=self.reasoning_agent
                                )
        self.crew = Crew(
                    agents=[self.reasoning_agent],
                    tasks=[self.reasoning_task],
                    process="sequential",
                    verbose=True
                    )
    def run(self,query:str):
        'Run the agnet'
        decision_crew = Crew(
            agents=[self.decider],
            tasks=[self.decision_task],
            process="sequential",
            verbose=True
        )
        decision = decision_crew.kickoff(inputs={"query": query})
        print(f"[Decider] Decision: {decision}")
        if "Save" in str(decision):
            return self.websitesaver_tool._run(website=query)

        elif "Query" in str(decision):
            return self.crew.kickoff(inputs={"query": query})

        else:
            return f"⚠️ Unknown decision: {decision}"

if __name__=="__main__":
    obj=Myagent()
    print('query')
    print(obj.run(query='which are the (ODA)-eligible countries'))
    print('save')
    print(obj.run(query='save website https://www.chathamhouse.org/topics/refugees-and-migration'))
    # retriever = Retriever()
    # results = retriever.retrieve("ODA countries")
    # print(results)
    