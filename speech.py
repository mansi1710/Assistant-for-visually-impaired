import speech_recognition as sr
import pyttsx3
from google.oauth2 import service_account

from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re
import nltk
from nltk.corpus import stopwords

from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

class speech_to_text():
    def __init__(self):
       en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
       ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
       self.recognizer = sr.Recognizer()
       self.microphone = sr.Microphone()
       self.engine = pyttsx3.init();
       self.engine.setProperty('voice', en_voice_id)
       self.credentials = service_account.Credentials.from_service_account_file('api-key.json')


    def recognize_speech_from_mic(self):
        print("Start...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        print("Found mic")
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"
        if(response["transcription"]=="None"):
            print("Speech not detected! Pls try again!")
        return response["transcription"]

    def clean(self, text):
        lem = WordNetLemmatizer()
        stem = PorterStemmer()
        stop_words = set(stopwords.words("english"))
        new_words = ["hey", "hi", "hello", "what's up", "i", "please", "help", "using", "show", "result", "large",
                     "also", "iv", "one", "two", "new", "previously", "shown"]
        stop_words = stop_words.union(new_words) - {"whom", "who"}
        text = text.lower()
        text = text.split()
        ps = PorterStemmer()
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in
                                                            stop_words]
        text = " ".join(text)
        return text

    def text_speech(self, cleaned_text):
        self.engine.say(cleaned_text);
        self.engine.runAndWait();


