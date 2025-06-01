# HerbalTea Chatbot

This project is created to build a chatbot capable of consulting and taking care of customers of a herbal tea shop. 
![Product Name Screen Shot][product-screenshot]


## Key Features
* Run and expose API with Google Colab.
* Advise on the types of  tea products available in the store based on the customer's health status.
* Use of information from the tea shop's website 


## Pipeline (version 1)

![Pipeline][pipeline-screenshot]


## Pipeline (version 2)
![Pipeline2][pipeline-screenshot2]

## Setup 

### Run notebook file
- Import ['TeaChat.ipynb'](TeaChat.ipynb) to Google Colab or run locally.
- Replace ['gemini token']() and ['ngrok token']() with your tokens.
- Run all cells to expose your ngrok API.

### Paste your API into herbalTeaChatBot.py 
- Paste to this line
   ```sh
    st.session_state.flask_api_url_1 = "https://dd90-34-125-186-68.ngrok-free.app/v1/chat"  # Set your Flask API URL here
   ```

### Run 

```bash
streamlit run herbaltea_chatbot/herbatTeaChatBot.py
```

## Contact 
Tran Huy Hoang - [@huyhoangt2004](https://www.linkedin.com/in/huyhoangt2004/) - huyhoangt2202@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>




[product-screenshot]: images/screenshot.png
[pipeline-screenshot]: images/graph.png
[pipeline-screenshot2]: images/graph_v2.png
