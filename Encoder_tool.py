from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from AI_interactions import Credentials
from rank_bm25 import BM25Okapi
from chromadb import PersistentClient
import json

class Encoder():

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,
                            chunk_overlap=100,
                            separators=["\n\n", "\n", ".", " ", ""]
                        )
        self.cred=Credentials()
        self.chroma_client = PersistentClient(path="./chroma_store")
        self.collection = self.chroma_client.get_or_create_collection("donors")
        self.embedding = AzureOpenAIEmbeddings( azure_deployment="embedding-ada",
                                                openai_api_version="2023-05-15",
                                                api_key=self.cred.llm_api_key,
                                                azure_endpoint=self.cred.llm_base_url
                                                )  
        
        self.keyword_index = None
        self.a=[]

    def save_keywords(self, filename="keywords.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.documents_store, f, ensure_ascii=False, indent=2)

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

    
    # def query_retriver(self,top_k=5, alpha=0.5 ,query:str):
    #     cred=Credentials()
    #     chroma_client = Client()
    #     embedding = AzureOpenAIEmbeddings( azure_deployment="embedding-ada",
    #                                     openai_api_version="2023-05-15",
    #                                     api_key=cred.llm_api_key,
    #                                     azure_endpoint=cred.llm_base_url
    #                                     )   
    #     collection = chroma_client.get_or_create_collection("donors")
    #     query_vec = embedding.embed_query(query)
    #     vector_results = collection.query(
    #                                         query_embeddings=[query_vec],
    #                                         n_results=top_k
    #                                     )
    #     bm25_scores = bm25.get_scores(query.split())
    # bm25_ranked = sorted(
    #     list(enumerate(bm25_scores)),
    #     key=lambda x: x[1],
    #     reverse=True
    #     )[:top_k]

    # # Normalize and combine scores
    # hybrid_results = {}
    
    # # Add vector results
    # for doc, score in zip(vector_results["documents"][0], vector_results["distances"][0]):
    #     hybrid_results[doc] = hybrid_results.get(doc, 0) + alpha * (1 - score)  # distance → similarity

    # # Add BM25 results
    # for idx, score in bm25_ranked:
    #     doc = chunks[idx]
    #     hybrid_results[doc] = hybrid_results.get(doc, 0) + (1 - alpha) * score

    # # Sort final results
    # final_results = sorted(hybrid_results.items(), key=lambda x: x[1], reverse=True)[:top_k]
    # return [doc for doc, _ in final_results]    

