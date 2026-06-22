def chunk_text(text, chunk_size = 500, overlap = 100):
    """
    Split text into overlapping chunks

    chunk_size: how many characters in each chunk

    overlap: how many characters to overlap between consecutive chunks  
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Grab the chunk
        chunk = text[start:end]

        # Only keep chunks that have meaningful content (not just whitespaces)
        if chunk.strip():
            chunks.append(chunk)

        # Move forard by (chunk_size - overlap) so the next chunk overlaps
        start += (chunk_size - overlap)

    return chunks


# This block only runs when you execute chunk_text.py directly
# NOT when another script imports it
if __name__ == "__main__":

    # Loading the cleaned text "UScons_cleaned.txt" and chunking it
    with open("UScons_cleaned.txt", "r", encoding="utf-8") as f:
        full_text = f.read()

    chunks = chunk_text(full_text)

    print(f"\nTotal chunks created: {len(chunks)}")

    print(f"\n--- Chunk 1 ---\n{chunks[0]}")
    print(f"\n--- Chunk 2 ---\n{chunks[1]}")
    print(f"\n--- Chunk 3 ---\n{chunks[2]}")

    # Show the overlapping thing is working
    print("\n\n--- Last 100 chars of chunk 1---")
    print(repr(chunks[0][-100:]))
    print("\n--- First 100 chars of chunk 2---")
    print(repr(chunks[1][:100]))