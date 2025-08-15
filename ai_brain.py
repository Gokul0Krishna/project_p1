import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
class brain():
    def __init__(self):
        'ai agnet'
        
        load_dotenv(dotenv_path=Path('.env'))
        self.llm_api_key=os.getenv("deepseekkey")
        self.model=ChatOpenAI(model="deepseek/deepseek-chat-v3-0324:free",
                              api_key=self.llm_api_key,
                              base_url="https://openrouter.ai/api/v1")
        
    def chatinput(self,ele:str):
        "give input to ai and gives the output back"
        
        response=self.model.invoke([HumanMessage(content=ele)])
        return response.content

# if __name__=="__main__":
#     obj=brain()
#     res=obj.chatinput(ele='HI who are you')
#     print(res)