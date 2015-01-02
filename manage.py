import time
import threading

import os
from PIL import Image
from pyfirmata import ArduinoMega, util


board = ArduinoMega('/dev/tty.usbmodem1421')

CENTER_LED = [{'r': board.get_pin('d:4:p'), 'g': board.get_pin('d:3:p'), 'b': board.get_pin('d:2:p')}, [0, 0, 0],
              [0, 0, 0]]

while True:
    os.system("screencapture -x screen.jpg")
    CENTER_LED[1] = CENTER_LED[2][:]

    im = Image.open('screen.jpg')
    rgb_im = im.convert('RGB')
    temp_r, temp_g, temp_b = rgb_im.getpixel((im.size[0] / 2, im.size[1] / 2))
    CENTER_LED[2][0] = float(temp_r) / 255
    CENTER_LED[2][1] = float(temp_g) / 255
    CENTER_LED[2][2] = float(temp_b) / 255

    step_r = (CENTER_LED[1][0] - CENTER_LED[2][0]) / 100
    step_g = (CENTER_LED[1][1] - CENTER_LED[2][1]) / 100
    step_b = (CENTER_LED[1][2] - CENTER_LED[2][2]) / 100

    # print(str(CENTER_LED[1][0]) + " " + str(CENTER_LED[2][0]))

    for n in range(1, 100):
        CENTER_LED[0]['r'].write(CENTER_LED[1][0] - step_r * n)
        CENTER_LED[0]['g'].write(CENTER_LED[1][1] - step_g * n)
        CENTER_LED[0]['b'].write(CENTER_LED[1][2] - step_b * n)
        time.sleep(0.005)