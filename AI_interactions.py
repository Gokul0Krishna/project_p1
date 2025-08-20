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


class Websitesaver(BaseModel):
    """Input schema for Websitesaver."""
    query: str = Field(..., description="url of a website")

# --- Tool definition ---
class WebsitesaverTool(BaseTool):
    name: str = "Website saver tool"
    description: str = "Stores the given data"
    args_schema: Type[BaseModel] = RagretrieverInput

    def _run(self,website:str,**kwargs)->str:
        """saves the given website."""
        


class Myagent(Retriever):
    def __init__(self):
        super().__init__()

        self.ragretriever_tool = RagretrieverTool()
        self.decider = Agent(
            role="Decider",
            goal="Decide which path to follow based on the reasoning output.",
            backstory="Acts like a traffic controller. Looks at reasoning results and chooses the right workflow branch.",
            llm=self.model,
            verbose=True
        )

        self.decision_task = Task(
            description=(
                "Look at the reasoning output: {reasoning_output}. "
                "Decide ONE path:\n"
                "- If it's factual knowledge → assign Summarizer.\n"
                "- If it looks like structured data / analysis → assign DB Analyst.\n"
                "Answer ONLY with the chosen role."
            ),
            expected_output="Either 'Summarizer' or 'DB Analyst'.",
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
        return self.crew.kickoff(inputs={"query": query})


# if __name__=="__main__":
#     obj=Myagent()
#     print(obj.run(query='which are the (ODA)-eligible countries'))
#     # retriever = Retriever()
#     # results = retriever.retrieve("ODA countries")
#     # print(results)
#     # retriever = RagretrieverTool()
#     # print(retriever._run(query="ODA countries"))