import streamlit as st
from ai_brain import brain
def main():
    ai=brain()
    st.title("prototype_V1")
    prompt = st.chat_input("Hello")
    if prompt:
        st.text(f"user:{prompt}")
        result=ai.chatinput(prompt)
        st.text(f'AI:{result}')

if __name__=='__main__':
    main()
