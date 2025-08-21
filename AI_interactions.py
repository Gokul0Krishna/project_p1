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
    """Input schema for Retriever."""
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

class P_S_saver_input(BaseModel):
    """Input schema for Proposal Suggestion saver."""
    jsn: str = Field(..., description="P_S_input")
class P_S_saver_Tool(BaseTool):
    name: str = " Proposal Suggestion saver tool"
    description: str = "Stores the given data"
    args_schema: Type[BaseModel] = P_S_saver_input
    def _run(self,jsn:str,**kwargs):
        """saves the given json"""
        with open('Proposal_Sugessions.txt','w') as file:
                    file.write(jsn)


class Myagent(Retriever):
    def __init__(self):
        super().__init__()

        self.ragretriever_tool = RagretrieverTool()

        self.websitesaver_tool = WebsitesaverTool()

        self.pssaver_tool=P_S_saver_Tool()
        
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
                                expected_output="Either 'Query' or 'Save'",
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
                                    description=(
                                        "Answer the user query: {query}. "
                                        "First, use the retriever tool to gather relevant donor-related context. "
                                        "Then, reason over it and return a structured response."
                                    ),
                                    expected_output=(
                                        "Return the output strictly as JSON in the following format:\n"
                                        "{\n"
                                        "  \"donors\": [\n"
                                        "    {\n"
                                        "      \"name\": \"<donor name>\",\n"
                                        "      \"info\": \"<summary about the donor>\",\n"
                                        "      \"past_projects\": [\n"
                                        "        {\"name\": \"<project name>\", \"funding\": \"<amount>\"},\n"
                                        "        ...\n"
                                        "      ]\n"
                                        "    }\n"
                                        "  ]\n"
                                        "}\n"
                                        "Only return valid JSON. No extra text.fill as much information as you can."
                                    ),
                                    agent = self.reasoning_agent,
                                    # output_key = "donor_json" 
                                )
        
        self.proposal_agent = Agent(
                                    role="Proposal Suggestion Maker",
                                    goal="Make tailored suggestions for proposals using structured donor information.",
                                    backstory="An expert at analyzing donor history and designing proposal strategies to maximize funding success.",
                                    llm=self.model,
                                    tools=[self.pssaver_tool],
                                    verbose=True
                                    )

        self.proposal_task = Task(
                                context=[self.reasoning_task],
                                description=(
                                    "You are given structured donor information in JSON format:\n"
                                    "For each donor, analyze their background and past projects, then suggest a proposal idea "
                                    "that aligns with their funding interests.\n\n"
                                    "Make your suggestions concise, actionable, and persuasive."
                                    "After creating the JSON, call the `Proposal Suggestion Saver` tool with the full JSON as input "
                                    "to save it to disk."
                                ),
                                expected_output=(
                                    "Return valid JSON in the following format:\n"
                                    "{\n"
                                    "  \"proposals\": [\n"
                                    "    {\n"
                                    "      \"donor\": \"<donor name>\",\n"
                                    "      \"suggestion\": \"<tailored proposal idea for this donor>\"\n"
                                    "      \"Reason\": \"<give the reason for the proposal(use the context)>\"\n"
                                    "    }\n"
                                    "  ]\n"
                                    "}\n"
                                    "Only output valid JSON, no extra text."
                                ),
                                agent=self.proposal_agent
                                )   

        

        self.resonarcrew = Crew(
                                agents=[self.reasoning_agent,self.proposal_agent],
                                tasks=[self.reasoning_task,self.proposal_task],
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
            return self.resonarcrew.kickoff(inputs={"query": query})
        else:
            return f"Unknown decision: {decision}"

if __name__=="__main__":
    obj=Myagent()
    print('query')
    print(obj.run(query='Find donors interested in migration and climate issues in Uk'))
#     print('save')
#     print(obj.run(query='save website https://www.chathamhouse.org/topics/refugees-and-migration'))
    # retriever = Retriever()
    # results = retriever.retrieve("ODA countries")
    # print(results)
    