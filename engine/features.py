import re
import eel
import webbrowser
from playsound import playsound
import pvporcupine
import pyaudio
from engine.command import speak
from engine.config import ASSISTANT_NAME, LLM_KEY
import os
import pywhatkit as kit
import struct
import pyautogui as autogui
import time

# newly added
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pyttsx3
import speech_recognition as sr

from engine.helper import extract_yt_term

import sqlite3
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# Register Chrome with its full path
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

@eel.expose
def playAssistantSound():
    music_dir = r"www\assets\start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.lower()
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")

    app_name = query.strip()
    if app_name!= "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (app_name.lower(),))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])
                 # [0][0] to remove the double brackets from the path given as result
            elif len(results) == 0:
                cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (app_name.lower(),))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " +query)
                    webbrowser.get('chrome').open(results[0][0])
                else:
                    speak("Opening "+ query)
                    try:
                        os.system('start '+ query)
                    except:
                        speak('not found')
        except:
            speak("some things went wrong")



def PlayYoutube(query):
    query = query.lower()
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't understand.")


def hotWord():
    porcupine = None
    paud = None
    audio_stream = None #backgroud microphone
    try:

        #pre-traied keywords
        porcupine = pvporcupine.create(keywords=["jarvis" , "alexa"]) #NLP based library
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate = porcupine.sample_rate , channels=1, format=pyaudio.paInt16 , input = True, frames_per_buffer=porcupine.frame_length)

        #loop for streaming to check for jarvis word being taken by the user
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h"*porcupine.frame_length , keyword)

            #processing keyword that comes from mic whether its alexa or jarvis or smth else
            keyword_index = porcupine.process(keyword)

            #checking first keyword detected or not
            if keyword_index >=0:
                print("hotword detected")

                #presssing shortcut key win+j
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# chat bot
import google.generativeai as genai
@eel.expose
def chatBot(query):
    try:
        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "")
        # Set your API key
        genai.configure(api_key=LLM_KEY)

        # Select a model
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Generate a response
        response = model.generate_content(query)
        filter_text = markdown_to_text(response.text)
        speak(filter_text)
    except Exception as e:
        print("Error:", e)


# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name

@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1

@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    con.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO sys_command VALUES (?, ?, ?)''', (None,key, value))
    con.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command VALUES (?, ?, ?)''', (None, key, value))
    con.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE Id = ?", (id,))
    con.commit()