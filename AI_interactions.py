import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import Agent, Task, Crew ,LLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings

from chromadb import Client
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

class HybridRetriever(Credentials):
    def __init__(self, docs):
       pass 





if __name__=="__main__":
    pass