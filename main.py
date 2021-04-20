import http.client, json
from PIL import Image, ImageDraw
import sys, os

KEY = ""

ENDPOINT = ""

request_url = "https://centralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=emotion"

face_detect_uri = "/face/v1.0/detect"

filename = "\\faces\\angry-face-lends-weight.jpg"

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = KEY
headers['Content-Type'] = "application/octet-stream"

uri_base = 'centralus.api.cognitive.microsoft.com'


def request_face_data(file_path, headers):
    try:
        photo_data = open(sys.path[0] + file_path, "rb").read()
    except Exception as e:
        print("Problem reading the file")
        print(e)

    try:
        connection = http.client.HTTPSConnection(uri_base)
        connection.request("POST", request_url, photo_data, headers)
        response = connection.getresponse()

        data = response.read().decode("utf-8")

        parsed = json.loads(data)

        emotions = parsed[0]['faceAttributes']['emotion']

        value = 0
        emotion_type = ''

        for key in emotions:
            if emotions[key] > value:
                value = emotions[key]
                emotion_type = key

        print("The displayed emotion is: " + emotion_type)
        image = Image.open(sys.path[0] + file_path)
        draw = ImageDraw.Draw(image)
        draw.text((30, 30), emotion_type, (0, 0, 0))
        image.show()

    except Exception as e:
        print("Problem with returned JSON")
        print(e)

photos = os.listdir('faces')

for photo in photos:
    request_face_data("\\faces\\" + photo, headers)
