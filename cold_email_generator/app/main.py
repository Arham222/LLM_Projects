import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chain import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    
    
    st.title("Cold Email Generator")
    url_input = st.text_input("Entera URL:", value="https://jobs.nike.com/job/R-32222")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills',[])
                links = portfolio.query_links(skills)
                email = llm.write_email(job, links)
                # st.text_area("mk",value = email,on_change=True,label_visibility="hidden")
                st.code(email,language="markdown",wrap_lines=True)
        except Exception as e:
            st.error(f"An Error Occured: {e}")



if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide",page_title="Cold Email Generator", page_icon="📧",initial_sidebar_state="expanded")
    create_streamlit_app(chain,portfolio,clean_text)
