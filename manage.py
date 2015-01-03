import threading
import time

import os
from PIL import Image
from pyfirmata import ArduinoMega


board = ArduinoMega('/dev/tty.usbmodem1421')


class LED:
    pins = None
    current_colors = [0, 0, 0]
    old_colors = [0, 0, 0]
    position = 0  # 1 - left, 2 - center, 3 - right
    board = None

    def __init__(self, board, pins, position):
        self.position = position
        self.board = board
        self.pins = [self.board.get_pin('d:' + str(pin) + ':p') for pin in pins]

    def update_colors(self, picture_name):
        while True:
            picture = Image.open(picture_name)
            self.old_colors = self.current_colors[:]

            pic_rgb = picture.convert('RGB')

            position_coords = {
                1: pic_rgb.getpixel((0, picture.size[1] / 2)),
                2: pic_rgb.getpixel((picture.size[0] / 2, picture.size[1] / 2)),
                3: pic_rgb.getpixel((picture.size[0] - 1, picture.size[1] / 2))
            }

            temp_colors = position_coords.get(self.position)

            self.draw(0, float(temp_colors[0])/100)
            self.draw(1, float(temp_colors[1])/100)
            self.draw(2, float(temp_colors[2])/100)
            time.sleep(0.1)

            # self.current_colors = [float(color) / 255 for color in temp_colors]
            #
            # step_r = (self.old_colors[0] - self.current_colors[0]) / 100
            # step_g = (self.old_colors[1] - self.current_colors[1]) / 100
            # step_b = (self.old_colors[2] - self.current_colors[2]) / 100
            #
            # for n in range(1, 50):
            #     self.draw(0, self.old_colors[0] - step_r * n)
            #     self.draw(1, self.old_colors[1] - step_g * n)
            #     self.draw(2, self.old_colors[2] - step_b * n)
            #     time.sleep(0.005)

    def draw(self, pin, value):
        self.pins[pin].write(float(value))


leds = []
leds.append(LED(board, [5, 7, 6], 1))
leds.append(LED(board, [10, 9, 8], 3))

threads = []

def make_screen():
    while True:
        os.system("screencapture -x screen.jpg")
        time.sleep(0.1)

th = threading.Thread(target=make_screen)
th.daemon = True
threads.append(th)

for led in leds:
    th = threading.Thread(target=led.update_colors, args=('screen.jpg',))
    threads.append(th)

for thread in threads:
    thread.start()

while threads[0].is_alive():
    threads[0].join(7)