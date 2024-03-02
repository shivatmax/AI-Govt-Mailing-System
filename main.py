from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
from datetime import datetime

def render_sidebar():
    st.sidebar.title("Anti Corruption Reporting Portal")
    language = st.sidebar.radio("Choose a language for the letter:", ("Hindi", "English"))
    user_name = st.sidebar.text_input("Enter Your Name:")
    user_email = st.sidebar.text_input("Enter Your Email:")
    contact_number = st.sidebar.text_input("Enter Your Contact Number:")
    state = st.sidebar.selectbox("Select State", ["Delhi", "Mumbai", "Kolkata", "Chennai"])

    districts = {"Delhi": ["Central Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi"],
                 "Mumbai": ["South Mumbai", "North Mumbai", "East Mumbai", "West Mumbai"],
                 "Kolkata": ["North Kolkata", "South Kolkata", "East Kolkata", "West Kolkata"],
                 "Chennai": ["North Chennai", "South Chennai", "East Chennai", "West Chennai"]}

    selected_district = st.sidebar.selectbox("Select District", districts.get(state, []))

    complaint_level = st.sidebar.selectbox("Complaint Level", ["Central", "State", "District"])

    authorities = {"Central": ["Central Vigilance Commission", "CBI"],
                   "State": ["Anti Corruption Bureau", "Directorate of Vigilance"],
                   "District": ["District Magistrate", "Superintendent of Police"]}
                   
    post_of_authority = st.sidebar.selectbox("Name of Authority", authorities.get(complaint_level, []))
    
    address = st.sidebar.text_area("Address")
    date_of_incident = st.sidebar.date_input("Date of Incident", datetime.now())
    description_of_incident = st.sidebar.text_area("Description of Incident (Please provide as much detail as possible)")
    digital_signature_file = st.sidebar.file_uploader("Upload Digital Signature", type=["jpg", "png"])
    relevant_document_file = st.sidebar.file_uploader("Upload Relevant Document", type=["pdf", "docx", "jpg", "png"])
    submit_button = st.sidebar.button("SUBMIT")
    inputs = [language, user_name, user_email, contact_number, post_of_authority, state, address, date_of_incident, description_of_incident, selected_district, complaint_level]
    return submit_button, inputs

def generate_letter_content(language, user_name, user_email, contact_number, post_of_authority, state, address, date_of_incident, description_of_incident, selected_district, complaint_level):
    Date = datetime.now().strftime("%d-%m-%Y")
    prompt_template = """
Compose a formal letter in {language}, addressed to the {post_of_authority} at the {complaint_level} in {selected_district} {state}, India. 
Follow the structured format and respectful tone customary in official Indian correspondence.

Applicant's Information:

Name: {user_name}
Full Address: {address}, {state}
\n
Date: {Date}
\n
Letter Content:

Start with a respectful salutation to the {post_of_authority}, such as 'Respected Sir/Madam,'.
Introduce yourself briefly in the opening paragraph, mentioning Applicant's name and address.
Clearly state the purpose of your letter. If it's a complaint, mention that you wish to register a formal complaint. If it's an inquiry, specify what information you seek.
Describe the incident: Provide a detailed account of the incident that occurred on {date_of_incident}, including what happened, where, and its impact on you or the community. 
Be concise and factual in your description to {description_of_incident}.
Request Action: Politely request a prompt investigation, resolution, or response to your inquiry or complaint. Specify any particular action you expect, such as corrective measures or the provision of information.
Conclude the letter by thanking the official for their attention to the matter and express your hope for a swift response.
Close with a respectful sign-off, such as 'Yours faithfully,' followed by your full name. Also, include my email - {user_email} and contact number- {contact_number} for further communication.
Ensure the letter is polite, professional, and underscores the urgency of a prompt resolution or response. Attach any relevant documents or evidence that supports your complaint or inquiry. 
"""
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key="AIzaSyDtjKJ2sVYCb-90ZQJs9n6RUYNnEHC5f7U")
    prompt = PromptTemplate.from_template(prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(language=language, user_name=user_name, user_email=user_email, contact_number=contact_number, post_of_authority=post_of_authority, state=state, date_of_incident=date_of_incident, description_of_incident=description_of_incident, Date=Date, address=address, selected_district=selected_district, complaint_level=complaint_level)
    return response.replace("**", "")

def display_main_content(submit, inputs):
    st.title("Letter Generation App")
    ai_generated_letter_placeholder = st.empty()
    if submit:
        generated_content = generate_letter_content(*inputs)
        ai_generated_letter_placeholder.text_area("AI-Generated Letter", generated_content, height=300)
        st.success("Your letter has been generated and submitted successfully.")
    else:
        ai_generated_letter_placeholder.text_area("AI-Generated Letter", "Your AI-generated letter content will appear here...", height=300)
    if st.button("SEND EMAIL", key="send_email"):
        st.success("Email has been sent successfully! (Dummy functionality)")

def main():
    submit, inputs = render_sidebar()
    display_main_content(submit, inputs[:])

if __name__ == "__main__":
    main()
