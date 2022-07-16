import json
import os
from urllib import response
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
from dotenv import load_dotenv
import math
import arabic_reshaper
import requests

load_dotenv()

# sign in to instagram
client = Client()
client.login(os.environ.get("USERNAME"), os.environ.get("PASSWORD"))

hashtags = "#بلوچ #بلوچی #بلوچستان #بلوچستانی #بلوچی_می_وتی_شهدین_زبان_انت #بلوچی_زبان #بلوچی_ادب  #زبان #بلوچستان #بلوچی_شعر#baloch #balochi #balouchistan #balouchestan #labz #balochistan #baluch"


def getTodaysID():
    EPOCH = 1657911600
    UNIX = dt.now().timestamp()
    id = int(math.floor((UNIX - EPOCH) / 86400))
    return id


def getWordImage():
    id = getTodaysID()
    url = f'http://balochi-api.herokuapp.com/api/sayadganj/id/{id}'

    myResponse = requests.get(url)

    myJson = json.loads(myResponse.text)
    width = 1080
    height = 1080
    font = ImageFont.truetype("arial.ttf", size=150)

    img = Image.new('RGB', (width, height), color='#112B3C')
    imgDraw = ImageDraw.Draw(img)

    char_to_replace = {'<h1>': '', '</h1>': ''}

    for item in myJson['data']:
        word = item['full_word']
        definition = item['definition']
        reshaped_word = arabic_reshaper.reshape(word)
        # Iterate over all key-value pairs in dictionary
        for key, value in char_to_replace.items():
            # Replace key character with value character in string
            definition = definition.replace(key, value)
        reversed_word = reshaped_word[::-1]  # slice backwards
        textWidth, textHeight = font.getsize(reversed_word)
        imgDraw.text(((width-textWidth)/2, (height-textHeight)/2),
                     reversed_word, font=font, fill=(255, 255, 255))
        img.save('./post/post.jpg')

    postImage(definition, hashtags)


def postImage(definition, hashtags):
    caption = f'{definition} \n\n -------- \n\n {hashtags}'
    try:
        client.photo_upload('./post/post.jpg', caption)
    except Exception as e:
        print(e)
    finally:
        print('Posted')


getWordImage()
