import io
from fitz import fitz, Rect
import requests
from util import getWebImage

def compositePdf(size, position, source, pageNo):
  request = requests.get(source["document"])
  filestream = io.BytesIO(request.content)

  document = fitz.open(stream=filestream, filetype="pdf")
  front_image = getWebImage(source["front"])
  back_image = getWebImage(source["back"])

  page = document[pageNo-1]

  # 計算縮放後的位置和大小
  front_position = (
    int(page.mediabox.width * position["front"][0] / size["document"][0]),
    int(page.mediabox.height * position["front"][1] / size["document"][1])
  )

  back_position = (
    int(page.mediabox.width * position["back"][0] / size["document"][0]),
    int(page.mediabox.height * position["back"][1] / size["document"][1])
  )

  front_size = (
    int(size["front"][0] * page.mediabox.width / size["document"][0]),
    int(size["front"][1] * page.mediabox.height / size["document"][1])
  )

  back_size = (
    int(size["back"][0] * page.mediabox.width / size["document"][0]),
    int(size["back"][1] * page.mediabox.height / size["document"][1])
  )

  front_rect = Rect(
    front_position[0], 
    front_position[1], 
    front_position[0] + front_size[0],
    front_position[1] + front_size[1]
  )

  back_rect = Rect(
    back_position[0], 
    back_position[1], 
    back_position[0] + back_size[0],
    back_position[1] + back_size[1]
  )
  
  front_image = front_image.resize(front_size)
  back_image = back_image.resize(back_size)

  stream = io.BytesIO()
  front_image.save(stream, format='PNG')
  stream.seek(0)
  front_image = stream.read()

  stream = io.BytesIO()
  back_image.save(stream, format='PNG')
  stream.seek(0)
  back_image = stream.read()
  
  page.insert_image(front_rect, stream=front_image)
  page.insert_image(back_rect, stream=back_image)
  return document
