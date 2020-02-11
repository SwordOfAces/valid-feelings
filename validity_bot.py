#!/usr/bin/env python3
import linecache
import os
import random
import re
import time

from PIL import Image, ImageDraw, ImageFont
import tweepy

def main():
    IMG_FILENAME = "feel_color.png"
    # Get absolute path of this file
    LOCATION = os.path.dirname(os.path.realpath(__file__)) + '/'
    cfg = get_config(LOCATION)
    api = get_api(cfg)
    valid_feelings = "feelings.txt"
    IMG_PATH = LOCATION + IMG_FILENAME 
    feeling, hexcolor = choose_feeling(valid_feelings)
    create_image(IMG_PATH, feeling, hexcolor)
    message = create_message(feeling)
    api.update_with_media(IMG_PATH, message)

def get_config(LOCATION):
    with open(LOCATION + 'keys') as keyFile:
        consumer_key = keyFile.readline().rstrip()
        consumer_secret = keyFile.readline().rstrip()
        access_token = keyFile.readline().rstrip()
        access_token_secret = keyFile.readline().rstrip()
    cfg = {}
    cfg['consumer_key'] = consumer_key
    cfg['consumer_secret'] = consumer_secret
    cfg['access_token'] = access_token
    cfg['access_token_secret'] = access_token_secret
    return cfg

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def choose_feeling(filename):
    with open(filename) as feelings:
        line_no = random.randint(1, len(feelings.readlines()) + 1)
    # Get that line from the file. 
    line = linecache.getline(filename, line_no)
    # Pull out the feeling and the color, ignore the frequency
    separator = re.compile(r'([a-z]+)\t\d+\t(\w+)')
    sepped = separator.search(line)
    feeling, hexcolor = sepped.groups()
    return feeling, hexcolor

def create_image(IMG_PATH, feeling, hexcolor):
    IMG_SIZE = 500
    FONT_PATH = r'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    FONT_SIZE = 55

    hash_hexcolor = '#' + hexcolor

    # Create the colored image.
    color_img = Image.new("RGB", (IMG_SIZE, IMG_SIZE), hash_hexcolor)
    draw = ImageDraw.Draw(color_img)
    font_used = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Determine sizes of text boxes.
    x_feel_sz, y_feel_sz = draw.textsize(feeling, font=font_used)
    x_color_sz, y_color_sz = draw.textsize(hash_hexcolor, font=font_used)

    # Position the text pieces.
    VERT_OFFSET = 36 # To separate the two rows.
    x_feel, y_feel = center_text(IMG_SIZE, x_feel_sz, y_feel_sz)
    y_feel -= VERT_OFFSET
    feeling_pos = x_feel, y_feel
    x_color, y_color = center_text(IMG_SIZE, x_color_sz, y_color_sz)
    y_color += VERT_OFFSET
    color_pos = x_color, y_color

    # Draw the text.
    draw.text(feeling_pos, feeling, fill='black', font=font_used)
    draw.text(color_pos, hash_hexcolor, fill='black', font=font_used)

    color_img.save(IMG_PATH)

    return None

def center_text(IMG_SIZE, x_size, y_size):
    x = (IMG_SIZE - x_size) // 2
    y = (IMG_SIZE - y_size) // 2
    return x, y

def create_message(feeling):
    frames = ["Current emotion: {0}",
                "I feel {0}",
                "I'm feeling {0}",
                "Currently feeling {0}",
                "feeling {0}",
                "current feel: {0}",
                "I'm feeling kinda {0}",
                "feeling {0} af",
                "feeling kind of {0} rn",
                "feeling {0} rn",
                "kinda {0} rn",
                "feeling sort of {0}",
                "feeling kinda {0} rn",
                "rn I'm feeling {0}",
                "feeling pretty {0}",
                "atm i'm feeling {0}",
                "feeling {0} atm",
                "feeling kind of {0} atm",
                "atm I'm feeling kinda {0}",
                "current emotion is {0}",
                "rn? i feel {0}"]
    message = random.choice(frames).format(feeling)
    return message

main()
