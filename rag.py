import os
import time

from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

import chromadb
from get_embedding_function import get_embedding_function

PROMPT_TEMPLATE = """

You are a helpful AI assistant. Your task is to answer the user's question based on the provided context. Include all 
relevant details from the context, even if some information appears slightly different or similar across multiple 
sources. Synthesize the information to provide a comprehensive and accurate answer.

Context:
{context}

Instructions:
1. Carefully read the question and all provided context.
2. Analyze all relevant information, including details that may be slightly different or similar across sources.
3. Synthesize the information to form a complete and accurate answer.
4. Include all relevant details in your response, even if they seem redundant.
5. If there are conflicting pieces of information, mention both and explain the discrepancy if possible.
6. If the context doesn't provide enough information to fully answer the question, state what is known and what 
information is missing.
7. Provide your answer in a clear, concise, and well-structured format.

---

Question: {question}

---
Answer:
"""

load_dotenv()
TOP_K = 5
llm = os.getenv("LLM")
embedding = os.getenv("EMBEDDING")
CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH")
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

model = Ollama(model=llm)
model.temperature = 0.3


def rag_query(query_text):
    # Prepare the DB.
    COLLECTION_NAME = f"{CHROMA_DATA_PATH}_{embedding.split('/')[0]}"
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=get_embedding_function(embedding))

    # RETRIEVAL
    retrieval_start_time = time.time()
    query_results = collection.query(query_texts=[query_text], n_results=TOP_K)
    retrieval_time = time.time() - retrieval_start_time
    # Create a list of dictionaries, each containing 'id' and 'distance'
    # ids represent the links of confluence pages retrieved.
    sources = [
        {'link': query_results['ids'][0][i], 'cosine_similarity': query_results['distances'][0][i]}
        for i in range(TOP_K)
        ]

    # AUGMENTATION
    context_text = "\n\n---\n\n".join(
            [doc['content'] for doc in query_results['metadatas'][0]])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # GENERATION
    generation_start_time = time.time()
    response_text = model.invoke(prompt)
    generation_time = round(time.time() - generation_start_time, 2)

    query_response_dict = {
        "llm": llm, "response": response_text,
        "sources": sources, "retrieval_time": retrieval_time,
        "generation_time": generation_time
        }
    print(query_response_dict)
    return query_response_dict


if __name__ == "__main__":
    query = "Example query"
    rag_query(query_text=query)