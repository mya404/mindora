# Mindora 💬

A simple student mental health companion chatbot built with Streamlit and Google Generative AI.

## About

Mindora is designed to provide supportive responses to students experiencing various emotional states. The chatbot detects mood from user input and offers personalized coping tips and encouragement.

**Supported moods:**
- Stress
- Anxiety
- Loneliness
- Low mood
- Balanced/Calm
- Crisis support

## Features

- 🎯 **Mood Detection**: Analyzes user messages to identify emotional state
- 🤖 **AI-Powered Responses**: Uses Google Gemini to generate warm, supportive replies
- 💡 **Coping Tips**: Provides practical mental health tips based on detected mood
- 💬 **Chat History**: Maintains conversation history during your session
- 🔄 **Fallback Responses**: Works without API key using pre-built supportive messages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mya404/mindora.git
cd mindora
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key (optional, for AI-powered responses):
   - Create a `.streamlit/secrets.toml` file in your project directory
   - Add your Google Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501` and start chatting with Mindora.

## Requirements

- Python 3.8+
- streamlit>=1.36,<2
- vaderSentiment>=3.3,<4
- google-genai>=0.8,<1

## How It Works

1. **Input**: You share how you're feeling
2. **Detection**: Mindora analyzes keywords and sentiment to detect your mood
3. **Response**: The chatbot provides an empathetic response (AI-generated or fallback)
4. **Support**: A personalized tip is provided to help you feel better

## Note

This chatbot is intended as a supportive companion tool. If you or someone you know is in crisis, please reach out to local emergency services or a mental health professional.

---

**Built with ❤️ for student mental health support**
