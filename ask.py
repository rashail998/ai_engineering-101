import anthropic
import chromadb
from chunk_text import chunk_text
from dotenv import load_dotenv
load_dotenv()

# Connect to already-built vector database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="us_constitution")

# Connect to claude
claude_client = anthropic.Anthropic()

print("\nChat with the US Constitution (type 'quit' to exit)\n")

while True:
    question = input("As a question: ")

    if question.lower() == "quit":
        break

    # 1. Retrieve relevant chunks from ChromaDB
    results = collection.query(
        query_texts = [question],
        n_results = 3
    )

    retrieved_chunks = results['documents'][0]

    # 2. Build context string from retrieved chunks
    context = "\n\n---\n\n".join(retrieved_chunks)

    # 3. Build the prompt
    prompt = f"""You are an expert on the United States Constitution.
    Answer the user's question using ONLY the context provided below.
    If the answer is not found in the context, say "I couldn't fin that in the provided context."
    DO NOT USE OUTSIDE KNOWLEDGE
    
    CONTEXT:
    {context}

    QUESTION:
    {question}


    ANSWER:"""

    # 4. Send to Claude
    response = claude_client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 500,
        messages = [{"role" : "user", "content" : prompt}]
    )

    print(f"\nAnswer: {response.content[0].text}\n")