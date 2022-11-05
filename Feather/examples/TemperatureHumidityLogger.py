# Temp logger
# James Crall, 2022

import adafruit_sdcard
import busio
import digitalio
import board
import storage

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D10)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

#Set up the real time clock
import adafruit_pcf8523
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(myI2C)
days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")


# Use the filesystem as normal.
t = rtc.datetime
print(t)

with open("/sd/test.txt", "w") as f:
    f.write("OK, now this?\n")
    print("is this thing on?")