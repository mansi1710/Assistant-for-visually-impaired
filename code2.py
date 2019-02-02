'''
from gtts import gTTS
import os
mytext = 'Hello!'
# Language in which you want to convert 
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")
os.system("welcome.mp3")
'''
import pyttsx3;
engine = pyttsx3.init();
engine.say("I will speak this text");
engine.runAndWait() ;