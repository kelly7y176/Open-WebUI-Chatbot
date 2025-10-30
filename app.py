import streamlit as st
import requests
import os
from requests.exceptions import RequestException

# --- Configuration & Setup ---

# Retrieve the public Tunnel URL from Streamlit Cloud Secrets
# Name of the secret must be 'OPEN_WEBUI_TUNNEL_URL'
API_BASE_URL = os.environ.get("OPEN_WEBUI_TUNNEL_URL")

# Retrieve the API Key from Streamlit Cloud Secrets (REQUIRED if Open WebUI has auth enabled)
# Name of the secret must be 'OPEN_WEBUI_API_KEY'
API_KEY = os.environ.get("OPEN_WEBUI_API_KEY", "")

# Check if the base URL is set. If not, stop the app with an error.
if not API_BASE_URL:
    st.error("Error: OPEN_WEBUI_TUNNEL_URL secret not found. Set your Cloudflare Tunnel URL in Streamlit Cloud Secrets.")
    st.stop()

# Define the full chat endpoint URL
CHAT_ENDPOINT = f"{API_BASE_URL}/api/v1/chat"

# Set API headers, including the Authorization header
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# --- Streamlit UI Setup ---

st.set_page_config(page_title="Remote Open WebUI Chat")
st.title(" 🚀 Remote AI Service (via Cloudflare Tunnel)")
st.caption(f"Connected to: {API_BASE_URL}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and API Logic ---

if prompt := st.chat_input("Enter your message to call Open WebUI..."):
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... Connecting to your local service via Tunnel..."):
            
            try:
                # Prepare the full message history for the API payload
                # Note: This is crucial for maintaining conversation context
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                # Construct the request body (payload)
                # IMPORTANT: Replace "llama3" with the actual model ID available in your Open WebUI setup
                payload = {
                    "model": "llama3",
                    "messages": api_messages,  # Send full history
                    "stream": False
                }
                
                # Send HTTP POST request
                response = requests.post(
                    CHAT_ENDPOINT,
                    json=payload,
                    headers=HEADERS, # Include the Authorization header
                    timeout=120
                )
                
                # Raise an exception for bad status codes (4xx or 5xx)
                response.raise_for_status()

                # Process the JSON response data
                response_data = response.json()
                
                # Extract the assistant's response content
                assistant_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Error: Could not parse API response.")
                
                st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except RequestException as e:
                # Handle connection failures, timeouts, DNS errors, etc.
                error_message = f"Connection Error: Please ensure Tunnel & Open WebUI are running. Details: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
            
            except Exception as e:
                # Handle general errors (JSON parsing, indexing, etc.)
                st.error(f"An unknown error occurred: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Unknown error: {e}"})
