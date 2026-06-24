import streamlit as st
import chromadb
import anthropic
from chunk_text import chunk_text
from pypdf import PdfReader
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title = "Chat with any PDF",
    page_icon = "📄"
)

st.title("📄 Chat with any PDF")
st.caption("Upload a PDF and ask questions about it. Answers are grounded strictly in your document.")

# Claude client (cached so they don't reload on every interaction)
@st.cache_resource

def get_claude_client():
    return anthropic.Anthropic()

claude_client = get_claude_client()

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:

    # Use the filename as a unique collection name
    collection_name = uploaded_file.name.replace(".pdf", "").replace(" ", "_").lower()[:50]

    # Build or load the vector index for this PDF
    @st.cache_resource(show_spinner = "Reading and indexing your PDF...")

    def build_index(file_name, file_bytes):
        # Write the uploaded file to a temp file PdfReader can read it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        # Extract text
        reader = PdfReader(tmp_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        os.unlink(tmp_path) # Clean the temp file

        # Chunk it
        chunks = chunk_text(full_text)

        # Build ChromaDB collection
        chroma_client = chromadb.EphemeralClient() # In memory, no persistence needed
        collection = chroma_client.get_or_create_collection(name="pdf_collection")
        collection.add(
            documents = chunks,
            ids = [f"chunk_{i}" for i in range(len(chunks))]
        )

        return collection, len(chunks)
    
    collection, num_chunks = build_index(uploaded_file.name, uploaded_file.getvalue())
    st.success(f"✅ Indexed {num_chunks} chunks from **{uploaded_file.name}**. Ask away!")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new question
    if question := st.chat_input("Ask a question about your PDF..."):

        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role" : "user", "content" : question})

        # Retrieve relevant chunks
        results = collection.query(query_texts = [question], n_results=3)
        retrieved_chunks = results['documents'][0]
        context = "\n\n---\n\n".join(retrieved_chunks)

        # Build grounded prompt
        prompt = f"""You are a helpful assistant that answers questions about a document.
        Answer the user's question using ONLY the context provided below.
        If the answer is not found in the context, say "I couldn't find that in the provided document."
        Do not use any outside knowledge.
        
        CONTEXT:
        {context}

        QUESTION:
        {question}

        ANSWER:"""

        # Call claude
        with st.chat_message("assistant"):
            with st.spinner("Searching the document..."):
                response = claude_client.messages.create(
                    model = "claude-sonnet-4-6",
                    max_tokens = 500,
                    messages = [{"role" : "user", "content" : prompt}]
                )
                answer = response.content[0].text
                st.markdown(answer)

        st.session_state.messages.append({"role" : "assistant", "content" : answer})

        # Show retrieved chunks
        with st.expander("📄 View retrieved source chunks"):
            for i, chunk in enumerate(retrieved_chunks):
                st.markdown(f"**Chunk {i+1}:**")
                st.text(chunk)
                st.divider()

    else:
        # Show instructions when no file is uploaded yet
        st.info("👆 Upload a PDF above to get started. Works with any document — legal contracts, research papers, textbooks, manuals.")
        st.session_state.messages = [] # Reset chat when no file loaded