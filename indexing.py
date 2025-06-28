from dotenv import load_dotenv
import os
import json
from uuid import uuid4
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import DistanceStrategy

load_dotenv()

ngrok_token = os.getenv('NGROK_TOKEN')
gemini_token = os.getenv('GEMINI_TOKEN')
pinecone_api = os.getenv('PINECONE_TOKEN')

# Load the `output.json` file
with open('data.json', 'r',encoding="utf8") as f:
    data = json.load(f)

introduction = "Giới thiệu về cửa hàng: HerbaZen - Thương hiệu trà thảo mộc hiện đại, hướng đến lối sống xanh và quan tâm đến sức khỏe."
warranty = " HerbaZen cam kết mang đến những sản phẩm trà thảo mộc nguyên chất, được tuyển chọn kỹ lưỡng từ các vùng nguyên liệu sạch, không chất bảo quản, an toàn và tốt cho sức khỏe."
note = """Lưu ý khi sử dụng các dòng trà HerbaZen: 
-Nên uống sau khi ăn sáng và trước khi ngủ 30 phút để đạt hiệu quả tốt nhất.
-Không dùng khi đói hoặc thay thế hoàn toàn nước uống hàng ngày.
-Phụ nữ mang thai và người mắc bệnh mãn tính nên tham khảo ý kiến bác sĩ trước khi sử dụng.
-Đối với trà cam quế đường phèn: Không nên uống quá nhiều vào buổi tối vì quế có thể gây kích thích nhẹ
-Đối với trà an mộng: Không nên uống khi lái xe, cần tỉnh táo, Không nên dùng cùng lúc với thuốc an thần (có thể gây buồn ngủ quá mức)
-Đối với trà hoa hồng đường nâu-Trà dịu hồng: Không dùng cho người đang bị cảm nóng, sốt và Người có cơ địa nóng trong nên hạn chế đường nâu
-Đối với trà dưỡng nhan: Không nên uống khi đang có dấu hiệu nóng trong (nổi mụn, nhiệt miệng), Người bị tiểu đường nên hạn chế hoặc bỏ các thành phần chứa đường
"""
categories = "Các loại sản phẩm/Trà trong cửa hàng đang bán: Hoa hồng đường phèn - Hồng Tâm An, Hoa cúc táo đỏ kỳ tử - Cúc Ngọc Dưỡng Huyết,Trà an mộng ngủ ngon, Hoa hồng đường nâu - Trà dịu hồng"
list_of_documents = []
for item in data: 
  content = item['title'] + " \nGiá tiền: " + item['Price'] + " \nNguyên liệu: " + item['ingredients'] + "\n Công dụng: " + item['uses'] + "\n Hướng dẫn sử dụng: " + item["how to use"] + "\nHạn sử dụng (HSD): " + item["HSD"] + "\n Số lượng: " + item['quantity']
  list_of_documents.append(Document(page_content=content))

list_of_documents.append(Document(page_content=introduction))
list_of_documents.append(Document(page_content=warranty))
list_of_documents.append(Document(page_content=note))
list_of_documents.append(Document(page_content=categories))

print(len(list_of_documents))



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