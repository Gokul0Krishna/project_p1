import streamlit as st
import subprocess
def main():
    st.title("prototype_V1")
    prompt = st.chat_input("Hello")
    if prompt:
        st.text("hahaha")

if __name__=='__main__':
    main()
    # subprocess.run(['python -m streamlit run Streamlit_app.py'])
