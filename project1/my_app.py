import streamlit as st
import json
from AI_interactions import Myagent

agent=Myagent()
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home","websites"])

if page == "Home":
    st.title('Chat bot')
    prompt = st.chat_input("Ask my anything")
    if prompt:
        st.write(f'user:{prompt}')
        v=agent.run(query=prompt)
        st.write('AI:')
        data = json.loads(v.raw)
        for p in data["proposals"]:
            with st.container():
                st.markdown(f"### 🏛️ {p['donor']}")
                st.write(f"**INFO📚:{p['Info']}**\n")
                for i in p['suggestions']:
                    st.write(f"**Suggestion:** {i['idea']}")
                    st.write(f"**Reason:** {i['reason']}")
                    st.write('\n')    
                st.divider()  # horizontal separato

elif page == "websites":
    st.title('websites')
    with open('websites.txt','r+') as file:
        for i in file:
            st.write(i)