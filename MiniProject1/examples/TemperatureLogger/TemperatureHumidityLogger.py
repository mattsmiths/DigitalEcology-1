# Temp logger
# James Crall, 2022

# Load the following libraries onto the circuitpython device:
#
# adafruit_bus_device
# adafruit_pcf8523
# adafruit_register
# adafruit_sdcard
# 

import adafruit_sdcard
import busio
import digitalio
import board
import storage
import adafruit_pcf8523
from adafruit_ms8607 import MS8607
from time import sleep

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D10)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Set up the real time clock
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(myI2C)

#Set up temp/humidity/pressure sensor
sensor = MS8607(myI2C)

#Set the filename to log data to
logger_filename = "/sd/logger.csv"

while True:
    t = rtc.datetime
    ds = str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday) +"_" + str(t.tm_hour) + "-" + str(t.tm_min) + "-" + str(t.tm_sec)
    ms = "," + "%.2f" % sensor.pressure + "," + "%.2f" % sensor.temperature + "," + "%.2f" % sensor.relative_humidity + "\n"
    print(ds+ms)
    
    #Write measurements to sd card
    with open("/sd/logger.csv", "a") as f:
            f.write(ds+ms)
    print("Date written to sd card!")
    
    #Wait for 30s before taking another measurement
    sleep(60)