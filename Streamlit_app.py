import streamlit as st
def printlist(lst):
    for i in lst:
        st.text(i)

def main():
    lit=[
    'https://www.gov.uk/government/statistics/statistics-on-international-development-final-uk-aid-spend-2022/statistics-on-international-development-final-uk-aid-spend-2022',
    'https://www.iom.int/funding-and-donors/united-kingdom',
    'https://publications.parliament.uk/pa/cm201314/cmselect/cmintdev/349/349vw07.htm',
    'https://www.oecd.org/en/publications/development-co-operation-profiles_04b376d7-en/united-kingdom_052bbc63-en.html',
    ]

    st.title("Websites")

    # Create two columns
    left, right = st.columns(2)  # left smaller, right bigger

    with left:
        with st.form("my_form"):
            printlist(lit)
            add = st.form_submit_button("add")
            if add:
                title = st.text_input(label="enter website link")
                if title:
                    lit.append(title)
                    st.rerun()
                    print(lit)
    with right:
        [st.text(i) for i in lit]


if __name__=='__main__':
    main()
