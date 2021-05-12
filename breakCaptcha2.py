# Text extraction

from google.cloud import vision_v1 as vision
import io, os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\MK_Lee\\Desktop\\capstone\\dulcet-library-313312-73b8f502260d.json"


client = vision.ImageAnnotatorClient()
path = './images/img4.jpg'


with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

price_candidate = []
card_number_candidate = []
date_candidate = []

response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    content = text.description
    content = content.replace(',','')
    print('\n"{}"'.format(content))


