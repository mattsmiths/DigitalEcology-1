# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_ltr329_ltr303 import LTR329
import neopixel

i2c = board.I2C()  # uses board.SCL and board.SDA

time.sleep(0.1)  # sensor takes 100ms to 'boot' on power up
ltr329 = LTR329(i2c)

#Set up neo
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

max_br = 10000
pixel.brightness = 1
pixel.fill((100,255,70))
while True:
    lt = ltr329.visible_plus_ir_light
    if lt > max_br:
        lt = max_br
        
    pixel.brightness = lt/max_br

