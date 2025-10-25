import streamlit as st
import requests
import os
from requests.exceptions import RequestException

OPEN_WEBUI_TUNNEL_URL
API_BASE_URL = os.environ.get("OPEN_WEBUI_TUNNEL_URL")


if not API_BASE_URL:
    st.error("Error: OPEN_WEBUI_TUNNEL_URL environment variable not found. Please set your Cloudflare Tunnel URL in Streamlit Cloud Secrets.")
    st.stop()


CHAT_ENDPOINT = f"{API_BASE_URL}/api/v1/chat"


st.set_page_config(page_title="Remote Open WebUI Chat")
st.title(" Remote AI Service (via Tunnel)")



if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Enter your message to call Open WebUI..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        with st.spinner("Thinking... Connecting to your local service via Cloudflare Tunnel..."):
            

            try:
                # Construct the request body (payload)
                # IMPORTANT: Replace "llama3" with the actual model ID you are using in your Open WebUI setup
                payload = {
                    "model": "llama3", 
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False # Set to False for a single, complete response
                }
                
                # Send HTTP POST request to the remote Tunnel URL
                response = requests.post(
                    CHAT_ENDPOINT,
                    json=payload,
                    timeout=120 # Allow a generous timeout for the local service to respond
                )
                
                # Raise an exception for bad status codes (4xx or 5xx)
                response.raise_for_status() 

                # Process the JSON response data
                response_data = response.json()
                
               
                assistant_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Could not parse API response.")
                
                st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except RequestException as e:
                # Catch errors related to the HTTP request (connection failure, timeout, etc.)
                error_message = f"Connection or API Error: Please ensure your Tunnel and local service are running. Error: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
            except Exception as e:
                # Catch other general errors (e.g., JSON parsing failure)
                st.error(f"An unknown error occurred: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Unknown error: {e}"})
