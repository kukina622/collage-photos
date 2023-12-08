from datetime import datetime
from flask import Flask, render_template, request, send_file
from service.image import compositeImage
from service.pdf import compositePdf
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
  document_type: "pdf" | "image"

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
  document_type = json["document_type"]

  if document_type == "pdf":
    page = json["page"]
    document = compositePdf(size, position, source, page)
    pdf_byte_array = BytesIO(document.write())
    pdf_byte_array.seek(0)
    return send_file(pdf_byte_array, as_attachment=True, download_name=datetime.now().strftime("%Y%m%d%H%M%S") + ".pdf")

  else:
    document_image = compositeImage(size, position, source)
    img_byte_array = BytesIO()
    document_image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return send_file(img_byte_array, as_attachment=True, download_name=datetime.now().strftime("%Y%m%d%H%M%S") + ".png")



if __name__ == "__main__":
  app.run()