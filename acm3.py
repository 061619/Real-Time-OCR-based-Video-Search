import streamlit as st
import cv2
import pytesseract
import numpy as np
import easyocr
import requests
import json
import tempfile
import pygame
from gtts import gTTS
from googletrans import Translator
import webbrowser
import googleapiclient.discovery
from sentence_transformers import SentenceTransformer
import speech_recognition as sr
import io

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# API Keys
YOUTUBE_API_KEY = "AIzaSyCarRi3NGS7bmU8fQ6o5dA-S-z9PQKJNd4"
GEMINI_API_KEY = "AIzaSyCcut0jba_NB9GIM7KIEPDPLCubpww_UP0"

# IP Camera URL
IP_CAMERA_URL = "http://10.53.150.98:8080/video"

# Initialize Speech Recognizer
recognizer = sr.Recognizer()

# Streamlit UI
st.title("📹 AI-Based Smart Video Search System")

# Function to process image
def process_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary  

# Function to extract text using EasyOCR
def extract_text(image):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)
    return " ".join([res[1] for res in results])

# Function to get latest YouTube video
def get_video(query):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(q=query, part="snippet", maxResults=5, type="video").execute()

    videos = [{"title": item["snippet"]["title"], "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"} for item in search_response.get("items", [])]

    if videos:
        best_video = videos[0]
        return best_video["title"], best_video["url"]
    return None, None

# Function to summarize using Gemini AI
def generate_with_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    data = {"contents": [{"parts": [{"text": f"Summarize the key information from this text:\n{text}"}]}]}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Error processing response."
    return f"API Error: {response.status_code}"

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Function to convert text to speech
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

# Function to play audio
def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

# Function to get text from voice
def get_text_from_voice():
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        audio = recognizer.listen(source)

    response = requests.post('https://asr.iitm.ac.in/internal/asr/decode', files={'file': ('command.wav', io.BytesIO(audio.get_wav_data(convert_rate=16000, convert_width=2)), 'audio/wav')})

    if response.status_code == 200:
        return response.json().get("transcript", "Error processing speech")
    else:
        return "Speech recognition failed."

# Streamlit UI for input selection
option = st.radio("Choose Input Method:", [" Scan Headline (OCR)", " Speak (Voice Command)"])

if option == " Scan Headline (OCR)":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        processed_image = process_img(img)
        extracted_text = extract_text(processed_image)
        st.write(f"Extracted Text: {extracted_text}")

elif option == "Speak (Voice Command)":
    if st.button("Start Listening"):
        extracted_text = get_text_from_voice()
        st.write(f"Transcribed Text:{extracted_text}")

# If text is extracted, show options
if "extracted_text" in locals():
    choice = st.radio("Choose an option:", ["Watch Video", " Listen to Audio Summary"])

    if choice == "Watch Video":
        video_title, video_url = get_video(extracted_text)
        if video_title:
            st.write(f"Best Matched Video: {video_title}")
            st.video(video_url)
        else:
            st.write("No relevant video found.")

    elif choice == "Listen to Audio Summary":
        summary = generate_with_gemini(extracted_text)
        translated_text = translate_text(summary, "en")
        st.write(f"Summary:{translated_text}")
        speech_file = text_to_speech(translated_text, "en")
        st.audio(speech_file)
