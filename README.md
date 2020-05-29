# DobaraMatPuchana

## **Jyoti** : Assistant for blind

A *voice assistant* specifically aiming towards aiding the visually imapired.

This system is used to help the visually impaired to have access to the most important features enhancing their living conditions making use of different custom layouts and using speech to text.

More specifically, the system is a chat bot having features solely dedicated towards development of the visually impaired.

## Fetaures which make "Jyoti" unique:

The system consist of wearable headphones interfaced to Logitech webcam connected to Raspberry PI.

The system performs tasks based on the input (in form of speech) given by the user and responds back as speech.

Key Features:

1. **Description**:
  
    1. Jyoti gives a single line description of the surrounding details
    2. *Road Conditions*: Jyoti gives the user an overview of the road conditions, which would further the visually impaired accordingly.
    3. Jyoti also specifically mentions if the user is at common places like classrooms, kitchens, bedrooms, etc
    4. Responds the number of people, objects, etc in the frame of the webcam.

2. **Find**:

    1. Jyoti resonds to commands like *find my purse?*, *check if my watch is in this room?* depending upon whether @Entity is present in the frame of the camers
  
3. **Read**:

    1. Jyoti also detects text from images and reads it loud.
    2. As a further application it can summarize articles from newspapers. 
    
4. **Fill forms**
    
    1. Jyoti also reads out forms (majorly applicable for bank purposes)
    
5. **Mobile Interactions**

    1. It can read out notifications from mobile and as a further application respond to messages, emails, calender, etc
    
6. **Add ons**

    1. Jyoti serves the basic features of a chat bot i.e. responds to question including time, lighting conditions, basic wh questions, etc.
    
    
Tech- stacks used:

    1. SpeechRecognizer, Google API for speech to text conversion
    
    2. Python Text to Speech https://pypi.org/project/pyttsx3/
    
    3. Object Recogniiton using *COCO Dataset*
    
    4. Google Cloud Vision API 
    
    5. Dialogflow
            
 Install Dependencies
 Download the credential for Google Vision API.
 Copy and paste the files at thr required position.
 
 ```
    git clone https://github.com/mansi1710/DobaraMatPuchana
    cd DobaraMatPuchana
    pip install -r requirements.txt
 ```
 
 Run Code:
 
 ```
 python main.py
 ```
