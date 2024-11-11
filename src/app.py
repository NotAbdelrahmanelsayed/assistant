import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'F:\resume\assistant\bedo-elsayed-9228df9baa68.json'
from matcher import main_matcher, triggers, executables

from AppOpener import open as _open # type: ignore
import speech_recognition as sr
import pyttsx3 # type: ignore
import pyautogui # type: ignore

def listen():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            # command = recognizer.recognize_whisper(model="base.en", audio_data=audio)
            # command = recognizer.recognize_google(audio_data=audio)
            command = recognizer.recognize_google_cloud(audio_data=audio)
            print(f"You said: {command}")
            return command.lower() if command else False
        except sr.UnknownValueError:
            print("Sorry, I did not understand.")
            return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def type_text(text):
    pyautogui.write(text)

def add_to_todo_list(item):
    with open('todo.txt', 'a') as file:
        file.write(f"{item}\n")
    speak(f"Added {item} to your to-do list.")

def main():
    while True:
        command = listen()
        if command:
            speak(f"you said: {command}")
            main_matcher(command)
        else:
            print(f"Ignore this command {command}")
        # if 'open' in command:
        #     _open("")
        #     open_chrome()
        # elif 'add to to-do list' in command:
        #     item = command.replace('add to to-do list', '').strip()
        #     add_to_todo_list(item)
        # elif 'exit' in command or 'quit' in command:
        #     speak("Goodbye!")
        #     break
        # else:
        #     speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()

