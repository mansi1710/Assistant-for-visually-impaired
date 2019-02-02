import speech_recognition as sr
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('api-key.json')

r = sr.Recognizer()
mic = sr.Microphone()
sr.Microphone.list_microphone_names()


def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    print("Start...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

response = recognize_speech_from_mic(r, mic)
text = response['transcription']
print(text)

### Speech to text done using Google-API

### Key-word extraction

from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re # import Regular Expression library
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
# Stopwords include larger number of prepositions, pronouns, conjunction etc in sentence

from nltk.tokenize import RegexpTokenizer
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer

lem = WordNetLemmatizer()
stem = PorterStemmer()
word = "inversely"
print("stemming:",stem.stem(word))
print("lemmatization:", lem.lemmatize(word, "v"))

stop_words = set(stopwords.words("english"))
new_words = ["hey","hi", "hello", "what's up","i","please","help", "using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown"]
stop_words = stop_words.union(new_words)-{"whom", "who"}

text = text.lower()
text = text.split()
ps=PorterStemmer()

lem = WordNetLemmatizer()
text = [lem.lemmatize(word) for word in text if not word in
            stop_words]

print(text)

describe = 0
read = 0

description = ["weather", "describe", "looking", "sun", "rain", "atmosphere", "outside", "light", "bright"]
people = ["people", "person", "whom", "who"]

### Keyword extraction from small sentences done
for word in text:
    if(word in description):
        describe=1
        break
    elif(word == 'read'):
        read = 1
        break