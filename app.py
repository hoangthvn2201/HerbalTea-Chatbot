import streamlit as st
import requests
import uuid
st.set_page_config(layout="wide") 


# Set up the Streamlit interface
page = st.title("HerbalTeaChat")
page = st.markdown("""
    API endpoint: /v1/chat
""")

st.session_state.flask_api_url_1 = "https://f87d-118-70-150-138.ngrok-free.app/v1/chat"  # Set your Flask API URL here

# Generate a random session ID
session_id = str(uuid.uuid4())

# Initialize chat history in session state
if "chat_history_v1" not in st.session_state:
    st.session_state.chat_history_v1 = []

# Display the chat history using chat UI
for message in st.session_state.chat_history_v1:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(key="chat", placeholder="What is up?"):
    # Add user message to chat history
    st.session_state.chat_history_v1.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the payload for the request
    payload = {
        "message": {"human":prompt},
        "context": st.session_state.chat_history_v1,
        "sessionId": session_id,
        "stream": True  # Enable streaming
    }

    # Stream the response from the Flask API
    with st.chat_message("assistant"):
        streamed_content = ""  # Initialize an empty string to concatenate chunks
        response = requests.post(st.session_state.flask_api_url_1, json=payload, stream=True)

        # Create a placeholder to update the markdown
        response_placeholder = st.empty()

        # Check if the request was successful
        if response.status_code == 200:
            
            # TODO 4
            # Loop through each chunk and add the content to the variable streamed_content
            # Don't forget to use markdown to print the result
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    streamed_content += chunk  # Concatenate each chunk
                    # Update the placeholder with the concatenated content in real-time
                    response_placeholder.markdown(streamed_content)
            

            # Once complete, add the full response to the chat history
            st.session_state.chat_history_v1.append({"role": "assistant", "content": streamed_content})
        else:
            st.error(f"Error: {response.status_code}")