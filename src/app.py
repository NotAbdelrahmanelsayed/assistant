import os
import logging
from matcher import OpenApps
import speech_recognition as sr
import pyttsx3

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')#, filename="logger.txt")

# Environment Configuration
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'F:\resume\assistant\bedo-elsayed-9228df9baa68.json'

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
    
    def listen(self):
        """
        Listen for a voice command and return the text.
        """
        with sr.Microphone() as source:
            logging.info("Listening for commands...")
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google_cloud(audio_data=audio)#, credentials_json="../bedo-*")
            logging.info(f"Command recognized: {command}")
            return command.lower()
        
        except sr.UnknownValueError:
            logging.info("Could not understand the audio input.")
            return ""

        except Exception as e:
            logging.error(f"Error in recognizing speech: {e}")
            return ""


    def speak(self, text):
        """
        Convert text to speech.
        """
        self.engine.say(text)
        self.engine.runAndWait()
    
    def handle_app_action(self, command, action):
        """
        Handle app openning commands
        """
        try:
            apps = OpenApps(command)
            apps.set_command(action)
            output = apps.execute_command()
            # self.speak(output)
            return output
        except Exception as e:
            error_message = f"Failed to {action} app: {e}"
            logging.error(error_message)
            self.speak(error_message)
            return error_message


def main():
    assistant = VoiceAssistant()

    while True:
        # command = assistant.listen()
        command = str(input("command: ")).lower()
        if "open" in command:
            logging.info(assistant.handle_app_action(command, "open"))
        elif "close" in command:
            logging.info(assistant.handle_app_action(command, "close"))
        elif "exit" in command or "quit" in command:
            assistant.speak("Goodbye!")
            break
        else:
            assistant.speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()