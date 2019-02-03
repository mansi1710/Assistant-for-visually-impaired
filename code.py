#api-key= ywQGP9COzS3uPJjY9Ks4FxyQJ86rxk1iETOKfwYW7HgS
#URL = https://gateway.watsonplatform.net/visual-recognition/api
import io
from google.oauth2 import service_account
from google.cloud import vision
class gcp__():
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file('aj.json')
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)
    def detect_labels(self, path):
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = self.client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels:')

        for label in labels:
            print(label.description)

    def detect_text(self, path):
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        print('Text:')
        textm = ""
        for text in texts:
            textm += text.description
            textm = textm+" "
            #print(' "{}"'.format(text.description))
        print(textm)


path = 'face.jpg'
r = gcp__()
r.detect_labels(path)

