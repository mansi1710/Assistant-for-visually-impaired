import speech_recognition as sr
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
       self.recognizer = sr.Recognizer()
       self.microphone = sr.Microphone()
    def recognize_speech_from_mic(self):
        print("Start...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
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
    def cleen(self, text):
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

        return text

response = speech_to_text()
text = response.recognize_speech_from_mic()
cleened_text = response.cleen(text)
print(cleened_text)


