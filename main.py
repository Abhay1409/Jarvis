import speech_recognition as sr
import webbrowser
import pyttsx3
import winsound  # for beep sound (Windows)
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

newsapi = "your_news_api_key_here"

def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

  

def beep():
    # Frequency (Hz), Duration (ms)
    winsound.Beep(1000, 150)  # short beep at 1kHz for 150ms


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="<Your Key Here>",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content    

def processcommand(c):
   
    
    if 'open youtube' in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'open stackoverflow' in c.lower():
        speak("Opening Stack Overflow")
        webbrowser.open("https://stackoverflow.com")
    elif 'open github' in c.lower():
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    elif 'open gmail' in c.lower():
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com") 
    elif 'open linkedIn' in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link) 
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title']) 

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)                    
        
if __name__ == "__main__":
    speak("Initializing JARVIS.....")
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Recognizing....")
                audio = r.listen(source, timeout=5, phrase_time_limit=1)
                word = r.recognize_google(audio)

                if word.lower() == "jarvis":
                    speak("Yes Sir, I am listening")
                    beep()  # play beep before recording next command

                    # Listen for command
                    with sr.Microphone() as source:
                        print("Activating jarvis... ")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        processcommand(command)

        except Exception as e:
            print(f"Error: {e}")
