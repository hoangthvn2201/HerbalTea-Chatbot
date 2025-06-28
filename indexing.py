from dotenv import load_dotenv
import os
import json
from uuid import uuid4

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from default_terms import INTRODUCTION, WARRANTY, NOTE, CATEGORIES
from utils import create_doc

load_dotenv()

gemini_token = os.getenv('GEMINI_TOKEN')
pinecone_api = os.getenv('PINECONE_TOKEN')

if __name__ == "__main__":

  list_of_documents = create_doc("data/data.json")

  uuids = [str(uuid4()) for _ in range(len(list_of_documents))]
  embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=gemini_token)

  index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

  vector_store = FAISS(
      embedding_function=embeddings,
      index=index,
      docstore=InMemoryDocstore(),
      index_to_docstore_id={},
  )
  vector_store.add_documents(documents=list_of_documents, ids=uuids)
  vector_store.save_local(r"C:\Users\huyho\OneDrive\Desktop\HerbalTea-Chatbot\data\faiss_index","tea")