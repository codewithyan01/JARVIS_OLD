import speech_recognition as sr
import webbrowser
#import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
# from gtts import gTTS
# import pygame
# import os
import asyncio
import edge_tts
from playsound import playsound
import os
from datetime import datetime
import psutil
import pyjokes
import pyautogui

recognizer = sr.Recognizer()
# engine = pyttsx3.init() 


# VOICE = "en-IN-NeerjaNeural"   # Indian female
# VOICE = "en-IN-PrabhatNeural"  # Indian male
# VOICE = "en-US-GuyNeural"
VOICE = "en-GB-RyanNeural"
rate = "-15%"
pitch = "-35Hz"

async def _speak(text):
    output_file = "voice.mp3"

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

    playsound(output_file)

    os.remove(output_file)

def speak(text):
    asyncio.run(_speak(text))

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()


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

def get_news():

    api_key = "77872eedf3b045e38357592cba4704f1"

    url = f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={api_key}"

    response = requests.get(url)

    data = response.json()

    if data["status"] != "ok":
        speak("Sorry sir, I couldn't fetch news.")
        return

    articles = data["articles"]

    if len(articles) == 0:
        speak("No news available right now sir.")
        return

    speak("Here are the top headlines sir.")

    for i in range(3):
        title = articles[i]["title"]
        speak(title)


def take_screenshot():
    image = pyautogui.screenshot()

    file_name = "screenshot.png"
    image.save(file_name)

    speak("Screenshot taken and saved sir.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        speak("Battery information is not available sir.")
        return

    percent = battery.percent
    plugged = battery.power_plugged

    status = "charging" if plugged else "not charging"

    speak(f"Battery is at {percent} percent and is currently {status}.")

def wish_me():

    now = datetime.now()

    hour = now.hour

    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%d %B %Y")
    day = now.strftime("%A")

    # Greeting according to time

    if 5 <= hour < 12:
        greeting = "Good morning"

    elif 12 <= hour < 17:
        greeting = "Good afternoon"

    elif 17 <= hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good night, it's late, you should get some rest"

    response = (
        f"{greeting} sir. "
        f"Today is {day}, {current_date}. "
        f"The current time is {current_time}."
    )

    speak(response)

def tell_time():

    now = datetime.now()

    current_time = now.strftime("%I:%M %p")

    speak(f"The current time is {current_time}")


def tell_date():

    now = datetime.now()

    current_date = now.strftime("%d %B %Y")

    speak(f"Today's date is {current_date}")

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        speak(f"Playing {song}")
        webbrowser.open(link)
    elif "time" in c.lower():
        tell_time()
    elif "date" in c.lower():
        tell_date()
    elif "news" in c.lower():
        get_news()
    elif "battery" in c.lower():
        battery_status()
    elif "joke" in c.lower():
        tell_joke()
    elif "screenshot" in c.lower():
        take_screenshot()
    elif "exit" in c.lower() or "quit" in c.lower():
        speak("Goodbye sir. Have a nice day!")
        exit()
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 




if __name__ == "__main__":
    speak("Initializing Jarvis....")
    greeted = False
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                # First time only
                if not greeted:
                    wish_me()
                    greeted = True

                else:
                    speak("Yes sir?How can I assist you?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("You said: " + command)
                    processCommand(command)


        except Exception as e:
            print("Error: {0}".format(e))


