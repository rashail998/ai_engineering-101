import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

# List all collections
collections = client.list_collections()
print("Collections in database: ", collections)

# Try to get our collection
collection = client.get_or_create_collection(name="us_constitution ")
print("Document count in collection: ", collection.count())

# Try a direct query
results = collection.query(
    query_texts = ["how many senators does each state get"],
    n_results = 3
)

print("\nRaw results:")
print(results)