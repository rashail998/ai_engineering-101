import chromadb
from chunk_text import chunk_text

# Load the cleaned text
with open("Uscons_cleaned.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# Chunk it
chunks = chunk_text(full_text)
print(f"\nTotal chunks created: {len(chunks)}")

# Setting up ChromaDB (runs locally, no server needed)
client = chromadb.PersistentClient(path="./chroma_db")

# A "collection" is like a table in a regular database
# get_or_create means: use existing one if it exists, create fresh if not

collection = client.get_or_create_collection(
    name="us_constitution",
)

# Add chunks to the collection
collection.add(
    documents=chunks,
    ids = [f"chunk_{i}" for i in range(len(chunks))]
)

print(f"\nSuccessfully indexed {len(chunks)} chunks into ChromaDB")
print("\nVector database saved to ./chroma_db folder")

# Quick test: search for something
test_query = "how many senators does each state get?"
results = collection.query(
    query_texts = [test_query],
    n_results = 3
)

print(f"\nTest query: {test_query}")
print("\nTop 3 most relevant chunks retrieved:\n")
for i, doc in enumerate(results['documents'][0]):
    print(f"--- Result {i+1} ---")
    print(doc)
    print()