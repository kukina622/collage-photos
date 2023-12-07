from datetime import datetime
from flask import Flask, render_template, request, send_file
from util import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024


@app.route("/", methods=['POST', "GET"])
def index():
  if request.method == "GET":
    data={
      "front": request.args.get("front", "").replace("&amp;", "&"),
      "back": request.args.get("back", "").replace("&amp;", "&"),
      "document": request.args.get("document", "").replace("&amp;", "&")
    }
  elif request.method == "POST":
    json = request.json
    data={
      "front": json.get("front", ""),
      "back": json.get("back", ""),
      "document": json.get("document", "")
    }
  return render_template("index.html", data=data)

@app.route("/composite", methods=['POST'])
def composite():
  """
  size: Dict
    - front: [width: int, height: int]
    - back: [width: int, height: int]
    - document: [width: int, height: int]

  position: Dict
    - front: [x: int, y: int]
    - back: [x: int, y: int]
  
  source: Dict
    - front: str
    - back: str
    - document: str

  """
  json = request.json
  size = json["size"]
  position = json["position"]
  source = json["source"]

  document_image = getWebImage(source["document"])
  front_image = getWebImage(source["front"])
  back_image = getWebImage(source["back"])

  # 計算縮放後的位置和大小
  front_position = (
    int(document_image.width * position["front"][0] / size["document"][0]),
    int(document_image.height * position["front"][1] / size["document"][1])
  )

  back_position = (
    int(document_image.width * position["back"][0] / size["document"][0]),
    int(document_image.height * position["back"][1] / size["document"][1])
  )

  front_size = (
    int(size["front"][0] * document_image.width / size["document"][0]),
    int(size["front"][1] * document_image.height / size["document"][1])
  )

  back_size = (
    int(size["back"][0] * document_image.width / size["document"][0]),
    int(size["back"][1] * document_image.height / size["document"][1])
  )

  front_image = front_image.resize(front_size)
  back_image = back_image.resize(back_size)

  # 在 document 上合成前景和背景
  document_image.paste(back_image, back_position)
  document_image.paste(front_image, front_position)

  # 將合成後的圖片上傳到指定的位置
  img_byte_array = BytesIO()
  document_image.save(img_byte_array, format='PNG')
  img_byte_array.seek(0)

  return send_file(img_byte_array, as_attachment=True, download_name=datetime.now().strftime("%Y%m%d%H%M%S") + ".png")



if __name__ == "__main__":
  app.run()