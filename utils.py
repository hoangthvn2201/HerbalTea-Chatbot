from langchain_core.documents import Document
import json
from default_terms import INTRODUCTION, WARRANTY, NOTE, CATEGORIES

def create_doc(data_path: str):
  try:
    with open(data_path, 'r',encoding="utf8") as f:
      data = json.load(f)
    list_of_documents = []
    for item in data: 
      content = item['title'] + " \nGiá tiền: " + item['Price'] + " \nNguyên liệu: " + item['ingredients'] + "\n Công dụng: " + item['uses'] + "\n Hướng dẫn sử dụng: " + item["how to use"] + "\nHạn sử dụng (HSD): " + item["HSD"] + "\n Số lượng: " + item['quantity']
      list_of_documents.append(Document(page_content=content))

    list_of_documents.append(Document(page_content=INTRODUCTION))
    list_of_documents.append(Document(page_content=WARRANTY))
    list_of_documents.append(Document(page_content=NOTE))
    list_of_documents.append(Document(page_content=CATEGORIES))

    return list_of_documents
  except FileNotFoundError:
    print("File not found!")