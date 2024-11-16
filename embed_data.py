import json
import os
import time

from dotenv import load_dotenv

import chromadb
from get_embedding_function import get_embedding_function

load_dotenv()
CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH")
db_client = chromadb.PersistentClient(CHROMA_DATA_PATH)
embedding = os.getenv("EMBEDDING")


def load_documents():
    return load_json_file(
            "data/confluence_data_processed_sections_split_no_html_tags.json"
            )


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# usage of embedding and vector db based on https://realpython.com/chromadb-vector-database/
def add_to_chroma(chunks):
    collection_name = f"{CHROMA_DATA_PATH}_{embedding.split('/')[0]}"
    collection = db_client.get_or_create_collection(
            name=collection_name,
            embedding_function=get_embedding_function(embedding),
            metadata={"hnsw:space": "cosine"},
            )

    # Add or Update the documents.
    existing_items = collection.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks:
        if chunk["link"] not in existing_ids:
            new_chunks.append(chunk)
    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        # Measure time to store embeddings.
        start_time = time.time()
        new_chunk_ids = [chunk["link"] for chunk in new_chunks]
        metadata_list = [
            {"content": item["content"], "link": item["link"], "title": item["title"]}
            for item in new_chunks
            ]
        collection.add(
                documents=[chunk["title"] + " " + chunk["content"] for chunk in new_chunks],
                ids=new_chunk_ids,
                metadatas=metadata_list,
                )
        end_time = time.time()
        embedding_and_persistence_time = end_time - start_time
        print(
                f"Embedding and Persistence Time: {embedding_and_persistence_time:.2f} seconds"
                )
    else:
        print("No new documents to add")


def dumb_db():
    documents = load_documents()
    documents = documents[:20]
    add_to_chroma(documents)


if __name__ == "__main__":
    dumb_db()