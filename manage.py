from pyfirmata import ArduinoMega, util
board = ArduinoMega('/dev/tty.usbmodem1421')

pinR = board.get_pin('d:4:p')
pinG = board.get_pin('d:3:p')
pinB = board.get_pin('d:2:p')

import os
import time
from PIL import Image

import time, threading


def foo(r=0, g=0, b=0):
	os.system("screencapture -x screen.jpg")

	old_r = r
	old_g = g
	old_b = b

	im = Image.open('screen.jpg')
	rgb_im = im.convert('RGB')
	r, g, b = rgb_im.getpixel((im.size[0]/2, im.size[1]/2))
	r = float(r)/255
	g = float(g)/255
	b = float(b)/255

	step_r = (old_r-r)/100
	step_g = (old_g-g)/100
	step_b = (old_b-b)/100

	for n in range(1, 100):
		pinR.write(old_r-step_r*n)
		pinG.write(old_g-step_g*n)
		pinB.write(old_b-step_b*n)
		time.sleep(0.005)

	# time.sleep(1)
	foo(r=r, g=g, b=b)
foo(0, 0, 0)