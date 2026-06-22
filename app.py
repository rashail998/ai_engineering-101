import streamlit as st
import chromadb
import anthropic
from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title = "Chat with the US Constitution",
    page_icon = "📜"
)

st.title("📜 Chat with the US Constitution")
st.caption("Ask any question about the US Constitution. Answers are grounded strictly in the document.")

# Initialize connections (cached so they don't reload on every interaction)
@st.cache_resource

def load_resource():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("us_constitution")
    claude_client = anthropic.Anthropic()
    return collection, claude_client

collection, claude_client = load_resource()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if question := st.chat_input("Ask a question about the Constitution..."):

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(question)

    # Add to history
    st.session_state.messages.append({"role" : "user", "content" : question})

    # RAG: Retrieve relevant chunks
    results = collection.query(
        query_texts = [question],
        n_results = 3
    )

    retrieved_chunks = results['documents'][0]
    context = "\n\n---\n\n".join(retrieved_chunks)

    # Build grounded prompt
    prompt = f"""You are an expert on the United States Constitution.
    Answer the user's question using ONLY the context provided below.
    If the answer is not found in the context, say "I couldn't find that in the provided sections of the Constitution."
    Do not use any outside knowledge.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:"""

    # Call Claude and stream the response
    with st.chat_message("assistant"):
        with st.spinner("Searching the Constitution..."):
            response = claude_client.messages.create(
                model = "claude-sonnet-4-6",
                max_tokens = 500,
                messages = [{"role" : "user", "content" : prompt}]
            )
            answer = response.content[0].text
            st.markdown(answer)

    # Add assistant response to history
    st.session_state.messages.append({"role" : "assistant", "content" : answer})

    # Show retrieved context in an expandable section
    with st.expander("📄 View retrieved source chunks"):
        for i, chunk in enumerate(retrieved_chunks):
            st.markdown(f"**Chunk {i+1}:**")
            st.text(chunk)
            st.divider()