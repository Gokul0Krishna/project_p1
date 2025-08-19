import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew ,LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from typing import Type
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

class RetrieverInput(BaseModel):
    """Input schema for HybridRetriever."""
    query: str = Field(..., description="The user query to search for relevant documents.")

# --- Tool definition ---
class RetrieverTool(BaseTool,Retriever):
    name: str = "HybridRetriever"
    description: str = "Fetches relevant documents from the vector database to support reasoning."
    args_schema: Type[BaseModel] = RetrieverInput

    def _run(self,**kwargs)->str:
        """Run retrieval with user query."""
        query = kwargs.get("query")
        docs = Retriever.retrieve(query)
        return "\n".join([d.page_content for d in docs]) if docs else "No documents found."


class Myagent(Retriever):
    def __init__(self):
        super().__init__()

        self.retriever_tool = RetrieverTool()

        self.reasoning_agent = Agent(
                                role="Reasoner",
                                goal="Answer user queries using retrieved context",
                                backstory="An expert at analyzing and summarizing knowledge from documents.",
                                llm=self.model,   # or another LLM
                                tools=[self.retriever_tool],  # give it the retriever tool
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
    def run(self):
        return self.crew.kickoff(inputs={"query": 'Which countries are ODA eligible?'})


if __name__=="__main__":
    ai=Myagent()
    print(ai.run())
    