import speech_recognition as sr
import webbrowser
import pyttsx3
import pyaudio
import numpy as np
import time
import musicLibrary
import requests
import wikipediaapi
import datetime
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "650f2130d38b44be90a78d8efc4ef039"
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='Jarvis/1.0 (https://yourwebsite.com; your-email@example.com)'
)

# Constants for clap detection
CLAP_THRESHOLD = 8000
CHUNK = 1024
RATE = 44100
CLAP_DETECTION_WINDOW = 0.5

# Initialize PyAudio for clap detection
p = pyaudio.PyAudio()

# Function to make Jarvis "speak" by saving an audio file
def speak(text):
    print(f"Jarvis: {text}")  # Print for debugging
    audio_file = "static/response.mp3"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()

def fetch_summary_from_wikipedia(query):
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary
    else:
        return "Sorry, I couldn't find any information on that topic."

def get_current_date_time():
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")
    time = now.strftime("%I:%M %p")
    speak(f"Today's date is {date} and the current time is {time}.")

def get_weather(city="Kolkata"):
    api_key = "52636b3fafca4fe99d6161027240310"
    base_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    
    response = requests.get(base_url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temp_c']
        condition = data['current']['condition']['text']
        wind_speed = data['current']['wind_kph']
        humidity = data['current']['humidity']
        
        weather_message = (f"The current temperature in {city} is {temperature}°C with {condition}. "
                           f"Wind speed is {wind_speed} kilometers per hour and humidity is {humidity}%.")
        
        speak(weather_message)
    else:
        speak("Sorry, I couldn't retrieve the weather information at the moment.")

def processCommand(command):
    print(f"Processing command: {command}")
    if 'open google' in command.lower():
        speak("Opening Google")
        webbrowser.open("http://www.google.com")
    elif "open youtube" in command.lower():
        speak("Opening YouTube...")
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command.lower():
        speak("Opening Facebook...")
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command.lower():
        speak("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")
    elif "open whatsapp" in command.lower():
        speak("Opening WhatsApp...")
        webbrowser.open("https://whatsapp.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find the song {song}")
    elif "news" in command.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=650f2130d38b44be90a78d8efc4ef039")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles[:5]:
                    speak(article['title'])
                    time.sleep(1)
            else:
                speak("No articles found.")
        else:
            speak("Error fetching news.")
    elif "what is" in command.lower() or "tell me about" in command.lower():
        topic = command.replace("what is", "").replace("tell me about", "").strip()
        summary = fetch_summary_from_wikipedia(topic)
        speak(summary)
    elif "date" in command.lower() or "time" in command.lower():
        get_current_date_time()
    elif "weather" in command.lower():
        if "in" in command.lower():
            city = command.lower().split("in")[-1].strip()
        else:
            city = "Kolkata"
        get_weather(city)
    elif "who created you" in command.lower():
        speak("Neelabhra created me")

if __name__ == "__main__":
    speak("Jarvis is ready. Waiting for your command.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for command...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                processCommand(command)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            speak("Speech service error.")
        except Exception as e:
            print(f"Error: {e}")










# import webbrowser
# import pyttsx3
# import requests
# import wikipediaapi
# import datetime
# import os

# engine = pyttsx3.init()
# newsapi = "650f2130d38b44be90a78d8efc4efc4"
# wiki_wiki = wikipediaapi.Wikipedia(
#     language='en',
#     extract_format=wikipediaapi.ExtractFormat.WIKI,
#     user_agent='Jarvis/1.0'
# )

# # Function to make Jarvis "speak" and save response as an audio file
# def speak(text):
#     print(f"Jarvis: {text}")
#     audio_file = "static/response.mp3"
#     engine.save_to_file(text, audio_file)
#     engine.runAndWait()
#     return text  # Returning text response

# def fetch_summary_from_wikipedia(query):
#     page = wiki_wiki.page(query)
#     if page.exists():
#         return page.summary
#     else:
#         return "Sorry, I couldn't find any information on that topic."

# def get_current_date_time():
#     now = datetime.datetime.now()
#     date = now.strftime("%B %d, %Y")
#     time = now.strftime("%I:%M %p")
#     return f"Today's date is {date} and the current time is {time}."

# def get_weather(city="Kolkata"):
#     api_key = "52636b3fafca4fe99d6161027240310"
#     base_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

#     response = requests.get(base_url)

#     if response.status_code == 200:
#         data = response.json()
#         temperature = data['current']['temp_c']
#         condition = data['current']['condition']['text']
#         return f"The current temperature in {city} is {temperature}°C with {condition}."
#     else:
#         return "Sorry, I couldn't retrieve the weather information."

# def processCommand(command):
#     print(f"Processing command: {command}")
    
#     if 'open google' in command.lower():
#         speak("Opening Google")
#         webbrowser.open("http://www.google.com")
#         return "Opening Google"
#     elif "open youtube" in command.lower():
#         speak("Opening YouTube")
#         webbrowser.open("https://youtube.com")
#         return "Opening YouTube"
#     elif "open facebook" in command.lower():
#         speak("Opening Facebook")
#         webbrowser.open("https://facebook.com")
#         return "Opening Facebook"
#     elif "open linkedin" in command.lower():
#         speak("Opening LinkedIn")
#         webbrowser.open("https://linkedin.com")
#         return "Opening LinkedIn"
#     elif "open whatsapp" in command.lower():
#         speak("Opening WhatsApp")
#         webbrowser.open("https://whatsapp.com")
#         return "Opening WhatsApp"
#     elif "weather" in command.lower():
#         return speak(get_weather())
#     elif "date" in command.lower() or "time" in command.lower():
#         return speak(get_current_date_time())
#     elif "who created you" in command.lower():
#         return speak("Neelabhra created me")
#     else:
#         return speak("Sorry, I didn't understand that.")

# if __name__ == "__main__":
#     speak("Jarvis is now running.")
