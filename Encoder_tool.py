from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from AI_interactions import Credentials
class Encoder():
    def chunking(self,text:str):
        cred=Credentials()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = splitter.split_text(text)
    embedding = AzureOpenAIEmbeddings( azure_deployment="embedding-ada", openai_api_version="2023-05-15")