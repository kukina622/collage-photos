import requests
from io import BytesIO
from PIL import Image

def getWebImage(url):
  response = requests.get(url)
  img = Image.open(BytesIO(response.content))
  return img