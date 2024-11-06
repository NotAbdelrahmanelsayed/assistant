from actions import open_chrome
import speech_recognition as sr
import pyttsx3
import pyautogui

def listen():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_whisper(model="base.en", audio_data=audio)
            print(f"You said: {command}")
            return command.lower()
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
        if 'open chrome' in command:
            open_chrome()
        elif 'add to to-do list' in command:
            item = command.replace('add to to-do list', '').strip()
            add_to_todo_list(item)
        elif 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()

