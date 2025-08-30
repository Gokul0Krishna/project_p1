from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import LLM
# from rank_bm25 import BM25Okapi
from chromadb import PersistentClient
# import json

class Encoder():

    def __init__(self):
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
        self.splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,
                            chunk_overlap=100,
                            separators=["\n\n", "\n", ".", " ", ""]
                        )
        self.chroma_client = PersistentClient(path="./chroma_store")
        self.collection = self.chroma_client.get_or_create_collection("donors")
        self.embedding = AzureOpenAIEmbeddings( azure_deployment="embedding-ada",
                                                openai_api_version="2023-05-15",
                                                api_key=self.llm_api_key,
                                                azure_endpoint=self.llm_base_url
                                                )  
        
        self.keyword_index = None
        self.a=[]

    def checking(self,website:str)->bool:
        'checkes if the website already exists'
        with open('websites.txt','r+') as file:
            for i in file:  
                i = i.replace('\n','')
                if website == i:
                    return False
            return True
        
    def chunking(self,text:str):
        return self.splitter.split_text(text)
        
    
    def embedder(self, chunks, source_id:str): 
        for i, chunk in enumerate(chunks):
            vector = self.embedding.embed_documents([chunk])[0]
            uid = f"{source_id}_chunk_{i}"

            # Store in Chroma
            self.collection.add(
                ids=[uid],
                embeddings=[vector],
                documents=[chunk],
                metadatas=[{"source": source_id}]
            )



