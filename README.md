# 🚀 Project Name
A brief, one-sentence description of what your project is (e.g., "A Streamlit-based chatbot powered by the OPEN_WEBUI API.").

# 🛠️ Setup and Installation
Follow these steps to get your project up and running locally.

### Prerequisites
* Python 3.x

# Installation

```
# Clone the repository
git clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName

# Install dependencies
pip install -r requirements.txt
```

# 🔑 API Key Configuration (Crucial Step)
This application requires an API key for the OPEN_WEBUI service to function. For security, the key is read from an environment variable and is never hardcoded in the source.

The application uses the following line to retrieve your key:

```
API_KEY = os.environ.get("OPEN_WEBUI_API_KEY", "")
```

### How to Set Your API Key
You must set the environment variable named OPEN_WEBUI_API_KEY before running the application.

### 1. Local Development (Linux/macOS)
Set the variable for your current terminal session:

```
export OPEN_WEBUI_API_KEY="YOUR_API_KEY_HERE"
```

### 2. Local Development (Windows - Command Prompt)

```
set OPEN_WEBUI_API_KEY="YOUR_API_KEY_HERE"
```

### 3. Streamlit Cloud / Other Platforms
If you are deploying to a service like Streamlit Community Cloud, use their Secrets Management interface to securely set the OPEN_WEBUI_API_KEY environment variable.

# ▶️ Running the Application
Once you have set your API key, you can run the application:
```
streamlit run app.py
```

(Adjust app.py to your main application file name)

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


