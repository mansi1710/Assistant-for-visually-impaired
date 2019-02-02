import functions
import yolopy
import cv2
import speech
import pyaudio
import wave


import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/abhinavj98/PycharmProjects/dotslash/DobaraMatPuchana/dfkey.json"

def play_file(fname):
    # create an audio object
    wf = wave.open(fname, 'rb')
    p = pyaudio.PyAudio()
    chunk = 1024

    # open stream based on the wave object which has been input.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

        # cleanup stuff.
    stream.close()
    p.terminate()


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        # print('=' * 20)
        # print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent.display_name,
        #     response.query_result.intent_detection_confidence))
        # print('Fulfillment text: {}\n'.format(
        #     response.query_result.fulfillment_text))
    return response.query_result.intent.display_name, response.query_result.fulfillment_text

def describeScene(cam, model, engine):
    ret, frame = cam.read()
    label = model.detectAndPrint(frame, args)
    #model.detectAndShow(frame, args)
    print(label)
    lbldict = {}
    for i in label:
        if i in lbldict:
            lbldict[i] += 1
        else:
            lbldict[i] = 1
    once = True
    length = len(lbldict)
    r = 0
    for i, j in lbldict.items():
        if once:
            if j != 1:
                engine.text_speech("There are")
            else:
                engine.text_speech("There is")
            once = False
        engine.text_speech("{} {}".format(j, i))
        r += 1
        if r != length:
            engine.text_speech("and")
    if (length == 0):
        engine.text_speech("No objects found")


labelsPath = "yolo/coco.names"
weightsPath = "yolo/yolov3.weights"
configPath = "yolo/yolov3.cfg"
args = {"threshold":0.3, "confidence":0.5}
project_id = "blindbot-4f356"
cam = cv2.VideoCapture(1)
engine = speech.speech_to_text()
model = yolopy.yolo(labelsPath, weightsPath, configPath)
listening = False
intent = None
while True:

    print(listening)
    if not listening:
        resp = engine.recognize_speech_from_mic()
        print(resp)
        if(resp != None):
            intent, text = detect_intent_texts(project_id, 0, [resp], 'en')
        if(intent == 'Jyoti' and resp!=None):
            listening = True

    else:
        engine.text_speech("What can I help you with?")
        intent = ''
        engine.text_speech("Listening")
        resp = engine.recognize_speech_from_mic()
        engine.text_speech("Processing")
        if(resp!=None):
            print(resp)
            intent, text = detect_intent_texts(project_id, 0, [resp], 'en')
        if intent == 'Describe':
            describeScene(cam, model, engine)
        elif intent == 'endconvo':
            print(text)
            listening = False
            engine.text_speech(text)
        elif intent == 'Brightness':
            engine.text_speech("It is {} outside".format((functions.getBrightness(cam))[0]))
        elif resp != 'None':
            engine.text_speech(text)

    ret, img = cam.read()
    cv2.imshow('frame', img)

    cv2.waitKey(100)