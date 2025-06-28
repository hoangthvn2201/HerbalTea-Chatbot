from dotenv import load_dotenv
import os
from uuid import uuid4
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from utils import create_doc
from pinecone import Pinecone
from langchain_community.retrievers import BM25Retriever

load_dotenv()

ngrok_token = os.getenv('NGROK_TOKEN')
gemini_token = os.getenv('GEMINI_TOKEN')
pinecone_api = os.getenv('PINECONE_TOKEN')

class Reranker:
  def __init__(self, pc_api, model = "bge-reranker-v2-m3"):
    self.pc = Pinecone(pc_api)
    self.model = model
  def compute_score(self, query, documents):
    results = self.pc.inference.rerank(
        model = self.model,
        query = query,
        documents = documents,
        parameters= {
            "truncate": "END",
        },
    )
    results_list =[]
    for r in results.data:
      results_list.append([r.score,r.document])
    return results_list
  
class Retriever:
  def __init__(self, gemini_token, pinecone_api):
    self.gemini_token = gemini_token
    self.pinecone_api = pinecone_api
    self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=gemini_token)
    self.semantic_retriever = FAISS.load_local(folder_path=r"C:\Users\huyho\OneDrive\Desktop\HerbalTea-Chatbot\data\faiss_index", index_name="tea",embeddings=self.embeddings, allow_dangerous_deserialization=True)
    self.bm25_retriever = BM25Retriever.from_documents(create_doc(data_path='data/data.json'), k = 10)
    self.reranker = Reranker(pinecone_api)

  def __call__(self,query):
    semantic_results = self.semantic_retriever.similarity_search(
      query,
      k=10,
    )
    bm25_results = self.bm25_retriever.invoke(query)

    content = set()
    retrieval_docs = []

    for result in semantic_results:
      if result.page_content not in content:
        content.add(result.page_content)
        retrieval_docs.append(result)

    for result in bm25_results:
      if result.page_content not in content:
        content.add(result.page_content)
        retrieval_docs.append(result)

    # pairs = [[query,doc.page_content] for doc in retrieval_docs]

    # scores = self.reranker.compute_score(pairs,normalize = True)
    results = self.reranker.compute_score(query, [doc.page_content for doc in retrieval_docs])
    scores = [r[0] for r in results]

    # Retrieve the parent document from the child chunk based on a threshold score.
    context_1 = []
    context_2 = []
    context = []
    parent_ids = set()
    for i in range(len(results)):
      # Relevance score >= 0.6 will be used as context type 1 (indicating higher relevance to the query)
      if scores[i] >= 0.6:
        context_1.append(results[i][1]['text'])
      # Relevance score >= 0.1 will be used as context type 2 (indicating medium to lower relevance to the query)
      elif scores[i] >= 0.1:
        context_2.append(results[i][1]['text'])
      # If the relevance score < 0.1, it indicates that there are no relevant documents.
    if len(context_1) > 0:
      print('Context 1')
      context=context_1
    elif len(context_2) > 0:
      print('Context 2')
      context=context_2
    else:
      print('No relevant context')
    return context