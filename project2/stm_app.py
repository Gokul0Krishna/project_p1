# from audio_control import Audio

# obj=Audio()
# while True:
#     x=obj.listen()
#     print(x)

import streamlit as st
from AI_agents import AI
ai=AI()
chats = {
        'user':[],
        'AI':[],
        }
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["call","chat"])

if page=='chat':
    st.title('Chat bot')
    if chats:
        for i in range(len(chats["AI"])):
            st.write(f'user:{chats['user'][i]}')
            st.write(f'AI:{chats['AI'][i]}')

    prompt = st.chat_input("Ask my anything")
    if prompt:
        st.write(f'user:{prompt}')
        result=ai.rn(query=prompt)
        st.write(f'AI:{result}')
        chats['user'].append(prompt)
        chats['AI'].append(result)

elif page=='call':
    st.title('Call bot') 
        # Place button inside the styled div
    st.markdown('<div class="centered-button">', unsafe_allow_html=True)
    if st.button("Click Me!", key="center_button"):
        st.success("🎉 You clicked the button!")
    st.markdown('</div>', unsafe_allow_html=True)