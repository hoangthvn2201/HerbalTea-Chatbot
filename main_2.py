from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyngrok import ngrok
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tool_calling import Retrieve
from prompts import TOOL_PROMPT, ANSWER_PROMPT
from retriever import Retriever
from fastapi.responses import StreamingResponse, JSONResponse

load_dotenv()

ngrok_token = os.getenv('NGROK_TOKEN')
gemini_token = os.getenv('GEMINI_TOKEN')
pinecone_api = os.getenv('PINECONE_TOKEN')

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_token, temperature=0.5)
agent = llm.bind_tools([Retrieve])
agentChain = TOOL_PROMPT | agent

answerModel = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_token, temperature=0.5)
answerChain = ANSWER_PROMPT | answerModel

retriever = Retriever(gemini_token=gemini_token, pinecone_api=pinecone_api)

ngrok.set_auth_token(ngrok_token)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: dict
    context: list = []

@app.post("/v1/chat")
async def chat_v1(req: ChatRequest):
    user_message = req.message
    chat_history = req.context
    stream = True

    history_string = "\n".join(
        [f"{m['role']} : {m['content']}" for m in chat_history]
    )
    agent_response = agentChain.invoke({"chat_history": history_string})

    if 'function_call' in agent_response.additional_kwargs:
        refine_query = agent_response.tool_calls[0]['args']['query']
        context = retriever(refine_query)
        source_information = "\n".join(context)

        if stream:
            def generate():
                for chunk in answerChain.stream({"query": refine_query, "source_information": source_information, "chat_history": history_string}):
                    yield chunk.content
            return StreamingResponse(generate(), media_type='text/plain')
        else:
            response = answerChain.invoke({"query": refine_query, "source_information": source_information, "chat_history": history_string})
            return JSONResponse({'response': response.content})
    else:
        if stream:
            def generate():
                for chunk in agent_response.content.split(" "):
                    yield chunk + " "
            return StreamingResponse(generate(), media_type='text/plain')
        else:
            return JSONResponse({'response': agent_response.content})