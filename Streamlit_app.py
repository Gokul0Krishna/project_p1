import streamlit as st
def form():
    with st.form("my_form"):
        st.write("Inside the form")
        user_name = st.text_input("Enter your name:")
        slider_val = st.slider("Form slider",min_value=1,max_value=20)
        submitted = st.form_submit_button("Submit")
        if submitted:
            return True

def main():
    st.title("prototype_V1")
    with st.form("my_form"):
        st.write("Inside the form")
        user_name = st.text_input("Enter your name:")
        slider_val = st.slider("Form slider",min_value=1,max_value=20)
        submitted = st.form_submit_button("Submit")
        if submitted:
            return True
if __name__=='__main__':
    main()
