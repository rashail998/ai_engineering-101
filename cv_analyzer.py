import streamlit as st
import anthropic
from pypdf import PdfReader
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

# Page confirguration
st.set_page_config(
    page_title = "CV Analyzer final boss level 999 🗿",
    page_icon = "🗿"
)

st.title("CV Analyzer final boss level 999 🗿")
st.caption("Upload the CV and see if the candidate is worth it or not! 👀")

# Claude client (Cached so they don't reload on every interaction)
@st.cache_resource

def get_claude_client():
    return anthropic.Anthropic()

claude_client = get_claude_client()

# File uploader
uploaded_file = st.file_uploader("Upload the CV (PDF only)", type="pdf")

# Enter the job description
job_description = st.text_area("Enter the job desciption...")

# Analyze button
analyze_button = st.button("Analyze CV 🔎")

# We only need to extract text from PDF so we don't need a vector database
# Jumping to text extraction now

# Only run if all three conditions are met
if uploaded_file is not None and job_description and analyze_button:

    # Write the uploaded file to a temp file PdfReader can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    # Extract text
    reader = PdfReader(tmp_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"


    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Build the prompt
    prompt = f"""You are a professional recruiter. The job requires:
        \n{job_description}\n
        Here is the candidate's CV:
        \n{full_text}\n
        Provide a highly concise, bulleted analysis of the qualities and gaps (maximum 3-4 bullet points per section).
        LASTLY, ALWAYS GIVE A FINAL VERDICT CONSIDERING EVERYTHING IN THE CV AND THE JOB DESCRIPTION IF CANDIDATE IS FIT, WORTH INTERVIEWING OR SIMPLY NOT FIT FOR THE ROLE.

        ANSWER:"""

    # Call Claude
    with st.chat_message("assistant"):
        with st.spinner("Doing the systeming..."):
            response = claude_client.messages.create(
                model = "claude-sonnet-4-6",
                max_tokens = 1000,
                messages = [{"role" : "user", "content" : prompt}]
            )

        answer = response.content[0].text
        st.markdown("### Analysis Result")
        st.markdown(answer)

    st.session_state.messages.append({"role" : "assistant", "content" : answer})
    os.unlink(tmp_path) # Clean the temp file

elif analyze_button:
    # User click analyze but hasn't filled everything in
    if uploaded_file is None:
        st.warning("Please upload a CV first.")
    if not job_description:
        st.warning("Please enter a job description first.")

