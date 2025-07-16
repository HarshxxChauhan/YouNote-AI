GenAI Research Assistant 🧑‍💻📚



GenAI Research Assistant is an AI-powered web application designed to assist users in summarizing, extracting, and understanding YouTube video content using Large Language Models (LLMs). Built with Python, Streamlit, and Google Gemini API (or OpenAI/Cohere API, as needed), this tool automates the process of generating structured research notes from lengthy YouTube videos. It is ideal for students, researchers, content creators, and professionals looking to speed up content consumption and note-taking tasks.

✨ Key Features

✅ YouTube Transcript Extraction:

Automatically fetches transcript data from public YouTube videos using youtube-transcript-api.

✅ AI-Powered Summarization:

Generates clear, concise, and structured summaries in bullet-point format within a set word limit using LLM models such as Google Gemini, OpenAI GPT, or Cohere Command.

✅ Chunking Logic for Large Inputs:

Handles large transcripts by dividing them into manageable chunks, ensuring LLM API token limits are respected.

✅ Streamlit Web App Interface:

Offers a clean, responsive, and interactive front-end powered by Streamlit.

✅ Environment Variable Configuration:

Supports API key management using .env files for secure local development.

✅ Modular Backend Logic:

Cleanly structured Python functions for video ID extraction, transcript parsing, chunking, and AI summarization.

🛠️ Technology Stack


Component	Technology/Service
Frontend	Streamlit
Backend Logic	Python
AI Model	Google Gemini API / OpenAI / Cohere
Transcript Extraction	YouTube Transcript API
Secrets Management	python-dotenv, Streamlit Cloud Secrets


🔐 Environment Variables Configuration

Variable Name	Required	Purpose
GOOGLE_API_KEY	Optional	For Google Gemini model
OPENAI_API_KEY	Optional	For OpenAI GPT models
CO_API_KEY	Optional	For Cohere Command models

💻 How It Works

User Input:

Paste a YouTube video link into the input box on the Streamlit app.

Transcript Fetching:

Uses youtube-transcript-api to fetch available subtitles/transcripts.

Chunking:

Breaks long transcripts into chunks of ~2000 characters to respect LLM token limits.

Summarization:

Sends each chunk to the configured AI API (Gemini/OpenAI/Cohere).

Display Summary:

Combines all responses into a complete, structured note document shown in the browser.

✅ Best Practices


Never hardcode API keys into app.py in public repositories. Use .env or cloud secret settings.

Respect API quota limits for Google, OpenAI, or Cohere APIs. Free tiers have restrictions.

Use smaller transcript chunks if running into token or quota issues.

📌 Known Limitations


Not all YouTube videos have transcripts available.

LLM summarization quality may vary based on the model used.

Large transcripts could take longer to process due to chunking.

📁 Project Structure


bash
Copy
Edit
GenAI-Research-Assistant/
├── app.py                # Main Streamlit application file
├── .env.example          # Template file for environment variables
├── requirements.txt      # Python dependencies
├── .gitignore            # Files/folders to ignore in Git
├── README.md             # Project documentation
