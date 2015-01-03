import time
import threading

import os
from PIL import Image
from pyfirmata import ArduinoMega, util


board = ArduinoMega('/dev/tty.usbmodem1421')

# CENTER_LED = [{'r': board.get_pin('d:4:p'), 'g': board.get_pin('d:3:p'), 'b': board.get_pin('d:2:p')}, [0, 0, 0],
# [0, 0, 0]]
# LEFTLED = [{'r': board.get_pin('d:5:p'), 'g': board.get_pin('d:7:p'), 'b': board.get_pin('d:6:p')}, [0, 0, 0],
#            [0, 0, 0]]
# RIGHTLED = [{'r': board.get_pin('d:10:p'), 'g': board.get_pin('d:9:p'), 'b': board.get_pin('d:8:p')}, [0, 0, 0],
#             [0, 0, 0]]


class LED:
    pins = None
    current_colors = [0, 0, 0]
    old_colors = [0, 0, 0]
    position = 1  # 1 - left, 2 - center, 3 - right
    board = None

    def __init__(self, board, pins, position):
        self.position = position
        self.board = board
        self.pins = [self.board.get_pin('d:' + str(pin) + ':p') for pin in pins]

    def update_colors(self, picture):
        self.old_colors = self.current_colors[:]

        position_coords = {
            1: picture.getpixel((0, im.size[1] / 2)),
            2: picture.getpixel((im.size[0] / 2, im.size[1] / 2)),
            3: picture.getpixel((im.size[0]-1, im.size[1] / 2))
        }

        temp_colors = position_coords.get(self.position)

        self.current_colors = [float(color) / 255 for color in temp_colors]

        step_r = (self.old_colors[0] - self.current_colors[0]) / 100
        step_g = (self.old_colors[1] - self.current_colors[1]) / 100
        step_b = (self.old_colors[2] - self.current_colors[2]) / 100

        for n in range(1, 100):
            self.draw(0, self.old_colors[0] - step_r * n)
            self.draw(1, self.old_colors[1] - step_g * n)
            self.draw(2, self.old_colors[2] - step_b * n)
            time.sleep(0.005)

    def draw(self, pin, value):
        self.pins[pin].write(value)

led_left = LED(board, [4, 3, 2], 1)
led_center = LED(board, [5, 7, 6], 2)
led_right = LED(board, [10, 9, 8], 3)

while True:
    os.system("screencapture -x screen.jpg")

    im = Image.open('screen.jpg')
    rgb_im = im.convert('RGB')

    led_left.update_colors(rgb_im)
    led_center.update_colors(rgb_im)
    led_right.update_colors(rgb_im)