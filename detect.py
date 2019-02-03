import io
from google.oauth2 import service_account
from google.cloud import vision
import dialogflow_v2 as dialogflow
import cv2

def detect_text(cam, engine):
    credentials = service_account.Credentials.from_service_account_file('aj.json')
    client = vision.ImageAnnotatorClient(credentials=credentials)
    ret, content = cam.read()
    cv2.imwrite('op.jpg', content)
    with io.open('op.jpg', 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(len(texts))
    print('Text:')
    textm = ""
    for i, text in enumerate(texts):
        engine.text_speech(text.description)
        textm += text.description
        textm = textm + " "
    print(textm)

def detect_form(cam, engine):

    credentials = service_account.Credentials.from_service_account_file('aj.json')
    client = vision.ImageAnnotatorClient(credentials= credentials)
    #content = cam.read()
    path = 'bank.jpg'
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    print('Text:')
    textm = ""
    for i, text in enumerate(texts):
        if(i==0):
            engine.text_speech("The form is entitled as")
        if(i==1):
            engine.text_speech("The form asks about these details")
        engine.text_speech(text.description)
        if("Official" in text.description):
            break
        textm += text.description
        textm = textm+" "
    print(textm)



def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

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
    cv2.imwrite('op.jpg',frame)
    credentials = service_account.Credentials.from_service_account_file('aj.json')
    client = vision.ImageAnnotatorClient(credentials= credentials)
    path = 'op.jpg'
    #path = 'road.jpg'
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    engine.text_speech("Description of the view")
    stop = 2
    for i,j in enumerate(labels):
        engine.text_speech(j.description)
        if(i == 1):
            break

    checkRoad(labels, engine)
    tellObjects(client, image, engine)

def checkRoad(labels, engine):
    road = 0
    car = 0
    motor_vehicle = 0
    bicycle = 0
    classroom = 0
    truck = 0
    traffic = 0
    face = 0
    for i, label in enumerate(labels):
        if (label.description == "Highway" or label.description == "Lane" or label.description == "Road"):
            road += 1
        if (label.description == "Car"):
            car += 1
        if (label.description == "Motor vehicle"):
            motor_vehicle += 1
        if (label.description == "Bicycle"):
            bicycle += 1
        if (label.description == "Truck"):
            truck += 1
        if (label.description == "Face"):
            face += 1
        if (label.description == "Classroom"):
            classroom += 1
        if (label.description == "Traffic"):
            traffic += 1
    if (road >= 1):
        if (car >= 1 or motor_vehicle >= 1 or bicycle >= 1 or truck >= 1 or traffic >= 1):
            engine.text_speech(
                "It seems you are walking on a road with vehicles. Beware! Do you want me to find people for help?")
        else:
            engine.text_speech("It seems the road you are walking on is quite safe. Yet beware.")
    if (classroom >= 1):
        engine.text_speech("You seem to be in a classroom!")


def tellObjects(client, image,  engine):
    objects = client.object_localization(
        image=image).localized_object_annotations
    print('Number of objects found: {}'.format(len(objects)))
    # engine.text_speech("I will tell you the objects near you")
    for object_ in objects:
        print('{} '.format(object_.name))
        # engine.text_speech(object_.name)
    lbldict = {}
    for i in objects:
        if i.name in lbldict:
            lbldict[i.name] += 1
        else:
            lbldict[i.name] = 1
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
