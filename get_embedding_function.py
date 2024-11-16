from chromadb.utils import embedding_functions

"""
Loads the embedding model used for generating vector representations of text data.
Feel free to add your customized embedding model.
"""


def get_embedding_function(model_name):
    print(f"Using model: {model_name}")

    model_configs = {
        "nomic-ai/nomic-embed-text-v1": {
            "trust_remote_code": True
            },
        "aari1995/German_Semantic_V3": {
            "trust_remote_code": True,
            "truncate_dim": 1024
            },
        "sentence-transformers/all-mpnet-base-v2": {},
        "intfloat/multilingual-e5-large-instruct": {},
        "jinaai/jina-embeddings-v2-base-de": {
            "trust_remote_code": True
            },
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": {},
        "thenlper/gte-large": {}
        }

    if model_name not in model_configs:
        raise ValueError(f"Unsupported model: {model_name}")
    return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name,
            **model_configs[model_name]
            )