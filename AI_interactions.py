import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew ,LLM
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
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
        

if __name__=="__main__":
    ret=Retriever()
    print(ret.retrieve('Which countries are ODA eligible?'))