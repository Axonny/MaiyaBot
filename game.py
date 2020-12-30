from PIL import Image,ImageDraw
from io import BytesIO
import random
import os

def get_img(name):
    return random.choice(os.listdir(f"img/{name}"))

def resize_image(input):
    image = Image.open(input)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    pix = image.load()
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))
    resize = image.resize((int(width*0.05),int(height*0.05)))
    resize = resize.resize((int(width),int(height)))

    bio = BytesIO()
    bio.name = 'image.jpeg'
    resize.save(bio, 'JPEG')
    bio.seek(0)
    return bio
