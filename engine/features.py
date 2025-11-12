import re
import eel
import webbrowser
from playsound import playsound
import pvporcupine
import pyaudio
from engine.command import speak
from engine.config import ASSISTANT_NAME
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

# Load Hugging Face model once at startup
model_id = "google/gemma-3-270m-it"
token = os.getenv("HF_TOKEN")

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True, token=token)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True).eval()
# ends

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
@eel.expose
def chatBot(query):
    print("Received query:", query)

    if not query.strip():
        speak("Please say something.")
        return

    try:
        messages = [
            {"role": "system", "content": "You are Jarvis, a helpful and friendly AI assistant."},
            {"role": "user", "content": query},
        ]

        # Create chat text
        chat_text = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=False
        )

        inputs = tokenizer(chat_text, return_tensors="pt").to(model.device)

        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.8,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id,
            )

        # Decode only the new tokens
        generated_text = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
        ).strip()

        if not generated_text:
            generated_text = "Sorry, I couldn’t understand that."

        print("Gemma:", generated_text)
        eel.receiverText(generated_text)
        speak(generated_text)

    except Exception as e:
        print("Error in chatBot:", e)
        speak("Sorry, there was a problem processing that.")
