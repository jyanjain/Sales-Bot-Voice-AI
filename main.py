import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv  
import os
import pyttsx3
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
import requests
from datetime import datetime

load_dotenv()

engine = pyttsx3.init()

SHEETY_API_URL = os.getenv("SHEETY_API_URL")

def voice_input():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.8

    with sr.Microphone() as source:
        print("Speak now (say 'exit' or 'thank you' to stop")
        engine.say("Speak now")
        engine.runAndWait()

        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=20)

        try:
            text = recognizer.recognize_google(audio)
            print("User: ", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""

def speak(text):
    print("ChatBot: ", text)
    engine.say(text)
    engine.runAndWait()

def log_to_google_sheet(user_input, bot_response):
    data = {
        "sheet1": {
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    try:
        response = requests.post(SHEETY_API_URL, json=data)
        if response.status_code == 200 or response.status_code == 201:
            print("Logged to Google Sheet")
        else:
            print(f"Logging failed {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def setup_llm():

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a helpful and knowledgeable **Sales Assistant AI** for **Crystal Group**, a leading cold chain logistics company in India with over 60 years of experience.

        Your job is to:
        - Understand customer inquiries
        - Ask relevant follow-up questions if needed
        - Answer confidently like a sales rep

        Company Info:
        - Crystal Group provides end-to-end cold chain logistics, including refrigerated trucks, reefer container rentals, cold storage, marine containers, and dark store solutions.
        - Pan-India service with warehousing hubs in Kolkata & Bhubaneshwar.
        - Website: http://www.crystalgroup.in | Phone: 02240352000
        - Motto: #WeKeepItFresh

        Always respond with clarity, professionalism, and a friendly sales tone. Be persuasive but not pushy. Ask for customer requirements if unclear.
        Keep the response short always answer in 3 lines maximum, and engaging."""),
         
        MessagesPlaceholder(variable_name="chat_history"),

        ("human", "{input}")
    ])

    llm = ChatGroq(model_name="llama3-8b-8192")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

    return chain


def run_chat():
    conversation = setup_llm()

    while True:
        user_input = voice_input()

        if any(phrase in user_input for phrase in ["exit", "thankyou", "bye", "quit", "no that's all"]):
            speak("Thank you for talking to Crystal Group. Have a great day!")
            break

        response = conversation.run(user_input)
        speak(response)
        log_to_google_sheet(user_input, response)

run_chat()