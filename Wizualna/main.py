#!usr/bin/env python3

from PIL import Image
import random

width = 0
height = 0


def encode(img_name):
    global width, height

    img = Image.open(img_name)
    pixels = img.load()
    gray = (127, 127, 127)
    black = (0, 0, 0)
    white = (255, 255, 255)

    width, height = img.size

    participant_1 = Image.new(mode="RGB", size=(width * 2, height))
    pixels_1 = participant_1.load()
    participant_2 = Image.new(mode="RGB", size=(width * 2, height))
    pixels_2 = participant_2.load()

    for h in range(height):
        for w in range(width):
            is_black = random.randint(0, 1)
            if pixels[w, h] == white:
                if is_black:
                    pixels_1[w * 2, h] = black
                    pixels_2[w * 2, h] = black
                    pixels_1[w * 2 + 1, h] = gray
                    pixels_2[w * 2 + 1, h] = gray
                else:
                    pixels_1[w * 2, h] = gray
                    pixels_2[w * 2, h] = gray
                    pixels_1[w * 2 + 1, h] = black
                    pixels_2[w * 2 + 1, h] = black
            elif pixels[w, h] == black:
                if is_black:
                    pixels_1[w * 2, h] = black
                    pixels_2[w * 2, h] = gray
                    pixels_1[w * 2 + 1, h] = gray
                    pixels_2[w * 2 + 1, h] = black
                else:
                    pixels_1[w * 2, h] = gray
                    pixels_2[w * 2, h] = black
                    pixels_1[w * 2 + 1, h] = black
                    pixels_2[w * 2 + 1, h] = gray

    participant_1.save('participant_1.png')
    participant_2.save('participant_2.png')


def decode(participant_1_name, participant_2_name):
    global width, height

    participant_1 = Image.open(participant_1_name)
    participant_2 = Image.open(participant_2_name)

    pixels_1 = participant_1.load()
    pixels_2 = participant_2.load()

    decode_image = Image.new(mode="RGB", size=(width * 2, height))
    pixels_decode = decode_image.load()

    for h in range(height):
        for w in range(width * 2):
            pixels_decode[w, h] = (
                pixels_1[w, h][0] + pixels_2[w, h][0],
                pixels_1[w, h][1] + pixels_2[w, h][1],
                pixels_1[w, h][2] + pixels_2[w, h][2]
            )

    decode_image.save('decode_image.png')


def main():
    encode('kod.png')
    decode('participant_1.png', 'participant_2.png')


if __name__ == "__main__":
    main()
