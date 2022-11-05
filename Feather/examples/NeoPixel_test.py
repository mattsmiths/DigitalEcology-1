# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython status NeoPixel red, green, blue example."""
import time
import board
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pixel.brightness = 0
br_itr = 0.1
delay = 0.01
col_iter = 2
rv = 255
gv = 0
bv = 255
while True:
    while rv > 0:
        rv = rv - col_iter
        gv = gv + col_iter
        bv = bv - col_iter
        time.sleep(delay)
        pixel.fill((rv, gv, bv))

    rv = 255
    gv = 0
    bv = 255

    print(pixel.brightness)
    if pixel.brightness < 1:
        pixel.brightness = pixel.brightness + br_itr
    else:
        pixel.brightness = 0
