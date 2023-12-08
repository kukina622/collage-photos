from util import getWebImage

def compositeImage(size, position, source):
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
  return document_image
