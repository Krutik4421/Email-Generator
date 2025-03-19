import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from text import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold email Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.google.com/about/careers/applications/jobs/results/87572842903675590-data-scientist-content-safety-platform?q=data&location=United%20States&target_level=EARLY")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    create_streamlit_app(chain, portfolio, clean_text)


