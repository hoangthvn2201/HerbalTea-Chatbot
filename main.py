from pyngrok import ngrok
from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from tool_calling import Retrieve
from prompts import TOOL_PROMPT, ANSWER_PROMPT
from retriever import Retriever
# from langchain.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel 

load_dotenv()

ngrok_token = os.getenv('NGROK_TOKEN')
gemini_token = os.getenv('GEMINI_TOKEN')
pinecone_api = os.getenv('PINECONE_TOKEN')

# LLM refine tool calling
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_token, temperature = 0.5)
agent = llm.bind_tools([Retrieve])
agentChain = TOOL_PROMPT | agent

# LLM answer model
answerModel = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_token, temperature = 0.5)
answerChain = ANSWER_PROMPT | answerModel

# define retriever
retriever = Retriever(gemini_token=gemini_token, pinecone_api=pinecone_api)

ngrok.set_auth_token(ngrok_token)

app = Flask(__name__)
CORS(app)

@app.route('/v1/chat', methods=['POST'])
def chat_v1():
    # Extract parameters from the request
    user_message = request.json.get('message', {})
    chat_history = request.json.get('context', [])
    stream = True  # Default to False if not provided

    print(f'Message: {user_message}')
    print(f'Chat History: {chat_history}')

    history_string = "\n".join(
      [
          f"{message['role']} : {message['content']}"
          for message in chat_history
      ]
    )
    agent_response = agentChain.invoke({"chat_history":history_string})

    print(agent_response)
    if 'function_call' in agent_response.additional_kwargs:
      print('Guide to Herbal Tea')
      refine_query = agent_response.tool_calls[0]['args']['query']
      print(f'REFINED: {refine_query}')
      context = retriever(refine_query)
      source_information = ""
      for doc in context:
        content = doc
        source_information += content + "\n"

      if stream:
        def generate():
          for chunk in answerChain.stream({"query": refine_query, "source_information": source_information, "chat_history":history_string}):
            yield chunk.content
        return app.response_class(generate(), mimetype='text/plain')
      else:
        reponse = answerChain.invoke({"query": refine_query, "source_information": source_information,"chat_history":history_string})
        return jsonify({'response': reponse.content})
    else:
      print('Guide to CHAT')
      if stream:
        def generate():
          for chunk in agent_response.content.split(" "):
            yield chunk + " "
        return app.response_class(generate(), mimetype='text/plain')
      else:
        return jsonify({'response': agent_response.content})
    
if __name__ == '__main__':
    # Start ngrok to tunnel the Flask app
    url = ngrok.connect(5000)
    print(f" * ngrok tunnel: {url}")
    # Start Flask app
    app.run(port=5000)