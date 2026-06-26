# AI Engineering Projects

A collection of AI-powered applications built while learning AI engineering.

## Projects

### 1. Conversational Chatbot (`chat.py`)
A multi-turn chatbot that maintains conversation history using the Anthropic Claude API.

### 2. AI Sales Data Analyst (`analyze.py`)
Analyzes a sales CSV using Pandas and returns structured JSON insights via Claude.

### 3. RAG — Chat with your data (`app.py`)
A Streamlit web app that lets you ask questions about any uploaded PDF.
Built using Retrieval-Augmented Generation (RAG):
- PDF text extraction with pypdf
- Text chunking with overlap
- Semantic search via ChromaDB vector database
- Grounded answers via Claude API

### 4. CV analyzer app - independent project (`cv_analyzer.py`)
An AI-powered recruitment tool that analyzes candidate CVs against a job description and returns a structured recruiter-focused assessment.
- Upload any CV as a PDF and paste a job description to get an instant analysis
- Returns structured output: matching strengths, skill gaps, and a final verdict (Strong Fit / Worth Interviewing / Not a Fit)
- Prompt engineered specifically for recruiter use cases — concise, bulleted output designed for fast decision making
- Built independently as a Phase 2 project after completing guided RAG and chatbot exercises
- Tech used: Streamlit, Anthropic Claude API, pypdf, Python

## Setup

1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it (Windows): `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API key:
ANTHROPIC_API_KEY=your-key-here
6. Run the Constitution app: `streamlit run app.py`

## Tech Stack
- Python
- Anthropic Claude API
- Pandas
- ChromaDB
- Streamlit
- pypdf