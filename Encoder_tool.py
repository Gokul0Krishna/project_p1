from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from AI_interactions import Credentials
from chromadb import Client
class Encoder():
    def chunking(self,text:str):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = splitter.split_text(text)
        return chunks
    def embedder(self,chunks):
        cred=Credentials()
        chroma_client = Client()
        embedding = AzureOpenAIEmbeddings( azure_deployment="embedding-ada",
                                        openai_api_version="2023-05-15",
                                        api_key=cred.llm_api_key,
                                        azure_endpoint=cred.llm_base_url
                                        )   
        collection = chroma_client.get_or_create_collection("donors")
        for i, chunk in enumerate(chunks):
            vector = embedding.embed_query(chunk)
            collection.add(
                ids=[f"chunk_{i}"],
                embeddings=[vector],
                documents=[chunk]
            )