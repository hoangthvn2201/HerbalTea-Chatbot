# 🌿 HerbaZen Chatbot Assistant

HerbaZen Chatbot Assistant is an intelligent virtual assistant designed for **HerbaZen**, a herbal tea brand. The assistant leverages Retrieval-Augmented Generation (RAG) to deliver accurate, conversational responses to customer queries about the brand's products, benefits, and herbal ingredients.

## 📌 Project Purpose

This chatbot aims to:
- Provide instant and accurate responses to customer questions about HerbaZen herbal teas.
- Educate users on the health benefits, ingredients, and proper usage of the teas.
- Improve customer experience and reduce the need for manual support.

---
## 🧠 System Architecture
```text
         [ User ]
            │
            ▼
      [ Flask API ]
            │
            ▼
[ Agent (Intent Classifier) ]
|-----------------------> Irrelevant => [ Gemini API only ]
            │
            ▼
   [ Hybrid Retriever ]
   ├─ BM25 Search (text-based)
   ├─ FAISS Vector Search (embedding-based)
   └─ BGE Reranker (improve result relevance)
            │
            ▼
[ Retrieved Context + User Query ]
            │
            ▼
   [ Gemini API (LLM) ]
            │
            ▼
      [ Response ]
```
![Pipeline2][pipeline-screenshot2]


---


### 🔧 Technologies Used:
- **Flask** – API backend
- **FAISS** – Vector search engine
- **BM25** – Traditional keyword-based retriever
- **BGE Reranker** – Improves ranking of search results
- **Gemini API** – Language model for response generation
- **Ngrok** – Expose local API to the internet
- **Agent Tool Calling** – Determines relevance to herbal tea context

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/hoangthvn2201/HerbalTea-Chatbot.git
cd HerbalTea-Chatbot
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Environment Variables
```bash
NGROK_TOKEN = "YOUR/NRGOK/TOKEN"
GEMINI_TOKEN = "GEMINI/API/TOKEN"
PINECONE_TOKEN = "PINECONE/API/TOKEN"
```
### 4. Setup FAISS vector store
```bash
python indexing.py
```


### 4. Start Backend Service to expose the chat API
```bash
python main.py
```
Copy the provided ngrok URL and use it as the public endpoint for your chatbot

### 5. (Optional) Using front-end interface with Streamlit
- Paste the exposed api to this line in app.py
   ```sh
    st.session_state.flask_api_url_1 = "https://dd90-34-125-186-68.ngrok-free.app/v1/chat"  # Set your Flask API URL here
   ```

### 6. (Optional) Run the interface 

```bash
streamlit run herbaltea_chatbot/app.py
```


## 📞 Contact

For questions, feedback, or contributions, please reach out via:

- 📧 **Email**: [huyhoangt2201@gmail.com](mailto:huyhoangt2201@gmail.com)  
- 🌐 **LinkedIn**: [@huyhoangt2004](https://www.linkedin.com/in/huyhoangt2004/) 

<p align="right">(<a href="#readme-top">back to top</a>)</p>




[product-screenshot]: images/screenshot.png
[pipeline-screenshot]: images/graph.png
[pipeline-screenshot2]: images/graph_v2.png
