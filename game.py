from PIL import Image,ImageDraw
from io import BytesIO
from ImageParser import YandexImage
import requests
import random

parser = YandexImage()

def save(name, link):
    with open(f"img/{name}","wb") as f:
        b = requests.get(link)
        f.write(b.content)

def generate_name():
    alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
    return "".join(random.choices(alphabet, k=20))

def get_img(name):
    images = parser.search(name, parser.size.large)
    name = generate_name() + ".jpg"
    save(name, images[random.randint(0, len(images) - 1)].url)
    return name

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
