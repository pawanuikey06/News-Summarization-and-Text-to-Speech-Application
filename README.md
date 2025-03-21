# News Summarization and Sentiment Analysis App

## Overview
This project is a **News Summarization and Sentiment Analysis** application that extracts news articles, summarizes them, performs sentiment analysis, and provides text-to-speech conversion in Hindi. The app is built using **FastAPI**, **Streamlit**, **NLTK**, **LangChain MistralAI**, and integrates with **Google Translator**.

## Features
- Fetch news from the web
- Summarize extracted news
- Perform sentiment analysis
- Extract keywords
- Convert summary to Hindi audio (TTS)
- Deployable on Hugging Face Spaces

## Tech Stack
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **NLP:** NLTK, YAKE, LangChain MistralAI
- **Translation:** Deep Translator
- **Text-to-Speech:** gTTS
- **Deployment:** Hugging Face Spaces

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/News-Summarization-App.git
cd News-Summarization-App
```

### 2. Create Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file and add:
```ini
MISTRAL_API_KEY=your_api_key
```

## Running the Application

### 1. Start FastAPI Backend
```sh
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start Streamlit Frontend
```sh
streamlit run app.py
```

## Deploying on Hugging Face Spaces

1. Create a **new space** on Hugging Face ([huggingface.co/spaces](https://huggingface.co/spaces))
2. Select **Streamlit** as the SDK
3. Push the project to the created space:
   ```sh
   git remote add hf https://huggingface.co/spaces/your-hf-space
   git push hf main
   ```



