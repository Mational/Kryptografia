#!usr/bin/env python3

from PIL import Image

width = 0
height = 0


def to_bin(wm):
    result = ""
    for character in wm:
        result += bin(ord(character))[2:].zfill(8)
    return result


def show_changes(org_pix, mod_pix, wm_len):
    global width, height
    counter = 0
    for h in range(height):
        for w in range(width):
            if counter > wm_len:
                return
            print("Original:", org_pix[w, h], "\tModified:", mod_pix[w, h])
            counter += 3


def decode(mod_pix, wm_len, wm_text_len):
    d = separate_wm(mod_pix, wm_len)
    result = ""
    for i in range(wm_text_len):
        result += chr(int("0b" + d[i * 8: (i + 1) * 8], 2))
    return result


def separate_wm(mod_pix, wm_len):
    global width, height
    result = ""
    counter = 0
    for h in range(height):
        for w in range(width):
            if counter > wm_len:
                return result[:len(result) - len(result) % 8]
            r, g, b = mod_pix[w, h]
            result += bin(r)[2:].zfill(8)[7]
            result += bin(g)[2:].zfill(8)[7]
            result += bin(b)[2:].zfill(8)[7]
            counter += 3


def main():
    global width, height
    img = Image.open('image.png')
    img_pixels = img.load()

    mod_img = img.copy()
    mod_pixels = mod_img.load()

    width, height = img.size

    wm = "Water Mark"
    wm_text_len = len(wm)
    wm = to_bin(wm)
    wm_len = len(wm)
    counter = 0

    for h in range(height):
        for w in range(width):
            if counter < wm_len:
                r, g, b = mod_pixels[w, h]
                r = bin(r)[2:].zfill(8)
                g = bin(g)[2:].zfill(8)
                b = bin(b)[2:].zfill(8)
                if counter < wm_len:
                    r = r[:7] + wm[counter]
                    counter += 1

                if counter < wm_len:
                    g = g[:7] + wm[counter]
                    counter += 1

                if counter < wm_len:
                    b = b[:7] + wm[counter]
                    counter += 1

                r = int("0b" + r, 2)
                g = int("0b" + g, 2)
                b = int("0b" + b, 2)
                mod_pixels[w, h] = (r, g, b)
    mod_img.save('image_with_water_mark.png')

    # Pokazanie faktycznych zmian w pikselach obrazu
    show_changes(img_pixels, mod_pixels, wm_len)
    print("Odczytany znak wodny:", decode(mod_pixels, wm_len, wm_text_len))


if __name__ == "__main__":
    main()
