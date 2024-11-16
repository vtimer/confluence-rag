import os

import pandas as pd
from dotenv import load_dotenv

import chromadb
from get_embedding_function import get_embedding_function

load_dotenv()
CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH")
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

TOP_K = 5
embeddings = []  # all embedding models to evaluate, DATA EMBEDDING IN DB should take place BEFORE this step!
queries_with_grounded_truth = [
    {
        "query": "example query",
        "number_all_relevant_sources": 3,  # number of sources that should be retrieved.
        "complexity_score": 1
        # 1: same wording as dataset,
        # 2: synonyms,
        # 3: contextual and equivocal variations (i.e., illness of employee or family member)
        }]
results = []
for embedding in embeddings:
    COLLECTION_NAME = f"{CHROMA_DATA_PATH}_{embedding.split('/')[0]}"
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=get_embedding_function(embedding))
    for query in queries_with_grounded_truth:
        query_results = collection.query(query_texts=[query["query"]], n_results=TOP_K)
        sources = query_results['ids'][0]
        for item in sources:
            results.append({
                "query": query["query"], "embedding": embedding,
                "number_all_relevant_sources": query["number_all_relevant_sources"],
                "complexity_score": query["complexity_score"], "source": item
                })

df = pd.DataFrame(results)
# relevance: sources can be relevant (1) or irrelevant (0) to the query. This should be manually evaluated in the
# document for the next evaluation step
df['relevance'] = ''

# headers: ['query', 'embedding', 'number_all_relevant_sources', 'complexity_score', 'source', 'relevance']
# for each query and embedding, the source should be MANUALLY evaluated on relevance (1: relevant, 0: irrelevant)
df.to_csv('query_embedding_source_relevance.csv', encoding='utf-8')