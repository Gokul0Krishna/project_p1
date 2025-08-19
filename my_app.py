import streamlit as st
from Scraper_tool import Scraper

scraper=Scraper()
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home","websites"])

if page == "Home":
    st.title('Chat bot')

elif page == "websites":
    st.title('websites')
    with open('websites.txt','r+') as file:
        for i in file:
            st.write(i)

                
