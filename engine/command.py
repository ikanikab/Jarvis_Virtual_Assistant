import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate',172)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        eel.DisplayMessage('listening...')
        r.pause_threshold = 1.5
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=15, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            eel.DisplayMessage("Listening timed out.")
            return ""


    try:
        print('recognizing')
        eel.DisplayMessage('recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        print("Recognition Error:", e)
        eel.DisplayMessage("I didn't catch that.")
        return ''
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message!=1:
        query = message
    else:
        query = takecommand()
    print(query)
    eel.senderText(query)

    if not query:
        return
    
    try: 
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube":
            from engine.features import PlayYoutube
            PlayYoutube(query)
        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")

    eel.ShowHood()
