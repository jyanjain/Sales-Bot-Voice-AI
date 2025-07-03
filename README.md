Voice AI Sales Assistant

This is a voice-enabled AI chatbot built with Python, LangChain, and LLMs. It takes spoken user input, responds with natural-sounding answers using LLMs, speaks back the responses, and logs the full conversation (including timestamps) to Google Sheets via Sheety API.

🔧 Features

- 🎙 Voice input using SpeechRecognition
- 🧠 LLM-powered conversation with memory (LangChain + Groq)
- 🗣 Text-to-speech voice response (pyttsx3)
- 📝 Google Sheets logging via Sheety API
- ⏱ Timestamps recorded for each conversation turn
- 🔄 Continuous loop until user exits

🛠 Setup Instructions

1. Clone the repo

git clone https://github.com/jyanjain/Sales-Bot-Voice-AI.git
cd Sales-Bot-Voice-AI

2. Install dependencies

3. Set up environment variables- 

Create a .env file with:
GROQ_API_KEY=your_groq_key_here 
SHEETY_API_KEY=your_api_key_here

4. Setup Google Sheet & Sheety
Make sure your Google Sheet has columns: user, bot, and time in row 1.

5. Run the bot
python main.py

📝 Example Sheet Entry
user	bot	time
Do you offer delivery?	Yes, we provide pan-India delivery of refrigerated...	2025-07-03 16:58:09

📦 Tech Stack
Python
LangChain
LLMs (Groq/OpenAI)
SpeechRecognition
pyttsx3
Sheety API
