import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'F:\resume\assistant\bedo-elsayed-9228df9baa68.json'
from matcher import OpenApps

from AppOpener import open as _open # type: ignore
import speech_recognition as sr
import pyttsx3 # type: ignore
import pyautogui # type: ignore

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
    
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            # command = recognizer.recognize_whisper(model="base.en", audio_data=audio)
            # command = recognizer.recognize_google(audio_data=audio)
            command = self.recognizer.recognize_google_cloud(audio_data=audio)
            print(f"You said: {command}")
            return command.lower() if command else False
        
        except sr.UnknownValueError:
            print("Sorry, I did not understand.")
            return ""

    def speak(self, text):
        """
        Convert text to speech.
        """
        self.engine.say(text)
        self.engine.runAndWait()
    
    def open_app(self, command):
        """
        Handle app openning commands
        """
        apps = OpenApps(command)
        apps.set_command("open")
        output = apps.execute_command()
        self.speak(output)
        return output

    def close_app(self, command):
        """
        Handle app closing commands
        """
        apps = OpenApps(command)
        apps.set_command("close")
        output = apps.execute_command()
        self.speak(output)
        return output


def main():
    assistant = VoiceAssistant()
    
    while True:
        # command = assistant.listen()
        command = "close whatsapp"
        if "open" in command:
            print(assistant.open_app(command))
        
        elif "close" in command:
            print(assistant.close_app(command))

        
        elif 'add to to-do list' in command:
            item = command.replace('add to to-do list', '').strip()
            assistant.add_to_todo_list(item)
        
        elif 'exit' in command or 'quit' in command:
            assistant.speak("Goodbye!")
            break
        
        else:
            assistant.speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()