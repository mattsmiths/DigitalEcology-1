# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython status NeoPixel red, green, blue example."""
import time
import board
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pixel.brightness = 0
br_itr = 0.1 #Bright iterator - how long to delay 
delay = 0.01 #Delay between updates to the color
col_iter = 2 #interval to update the color channels (within range of 0 - 255)

#Set initial values for colors
rv = 255
gv = 0
bv = 255
while True:
    while rv > 0:
    	#Step colors
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
