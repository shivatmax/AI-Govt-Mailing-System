import streamlit as st
from datetime import datetime
# import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

def render_sidebar():
    st.sidebar.title("Menu")
    language = st.sidebar.radio("Choose a language for the letter:", ("Hindi", "English"))
    user_name = st.sidebar.text_input("Name of User")
    post_of_authority = st.sidebar.selectbox("Post of Authority", ["Option 1", "Option 2", "Option 3"])
    state = st.sidebar.text_input("State (district/city/area)")
    address = st.sidebar.text_area("Address")  
    name_of_authority = st.sidebar.multiselect("Name of Authority", ["Authority 1", "Authority 2", "Authority 3"])
    date_of_incident = st.sidebar.date_input("Date of Incident", datetime.now())
    description_of_incident = st.sidebar.text_area("Description of Incident")
    digital_signature_file = st.sidebar.file_uploader("Upload Digital Signature", type=["jpg", "png"])
    relevant_document_file = st.sidebar.file_uploader("Upload Relevant Document", type=["pdf", "docx", "jpg", "png"])
    submit_button = st.sidebar.button("SUBMIT")
    return language, user_name, post_of_authority, state, address, name_of_authority, date_of_incident, description_of_incident, digital_signature_file, relevant_document_file, submit_button

def display_main_content(submit_button, inputs):
    st.title("Letter Generation App")
    ai_generated_letter_placeholder = st.empty()
    ai_generated_letter = ai_generated_letter_placeholder.text_area("AI-Generated Letter", "Your AI-generated letter content will appear here...", height=300)
    if st.button("SEND EMAIL", key="send_email"):
        st.success("Email has been sent successfully! (Dummy functionality)")
    if submit_button:
        generated_content = generate_letter_content(*inputs[:-1]) 
        ai_generated_letter_placeholder.text_area("AI-Generated Letter", generated_content, height=300)


def generate_letter_content(language, user_name, post_of_authority, state, name_of_authority, address, date_of_incident, description_of_incident):
    prompt_template = """
    Write a formal {language} letter addressed to the {name_of_authority} at {post_of_authority} in {state}.
    Name of Applicant: {user_name}. Your Address: {address}. Today Date: {today}.
    The letter should inquire about or complain regarding an incident that occurred on {date_of_incident}. 
    The incident is described as follows: {description_of_incident}. The letter should be polite, professional, and seek a prompt resolution or response. 
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
    prompt = PromptTemplate.from_template(prompt_template)
    chain = LLMChain(llm = llm, prompt = prompt)
    response = chain.run(language = language, user_name = user_name, post_of_authority = post_of_authority, state = state, name_of_authority = name_of_authority, date_of_incident = date_of_incident, description_of_incident = description_of_incident, today = datetime.now(), address = address)
    return response

def main():
    st.set_page_config(layout="wide")
    inputs = render_sidebar()
    submit_button = inputs[-1]
    display_main_content(submit_button, inputs)

if __name__ == "__main__":
    main()
