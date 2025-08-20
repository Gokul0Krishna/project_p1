import streamlit as st
from AI_interactions import Myagent
agent=Myagent
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home","websites"])

if page == "Home":
    st.title('Chat bot')
    prompt = st.chat_input("Ask my anything")
    if prompt:
        st.write(agent.run(query=prompt))

elif page == "websites":
    st.title('websites')
    with open('websites.txt','r+') as file:
        for i in file:
            st.write(i)

                
