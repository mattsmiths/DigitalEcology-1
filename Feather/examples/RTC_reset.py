#To set the time, manually set date below (line 15), change 'False' to 'True', and run once (CTRL + D in Mu). Once it has run, and reset the clock, switch back to Falsem, rerun, and the time be set and remain correct

import busio
import adafruit_pcf8523
import time
import board

myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(myI2C)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

if False:   # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022,  11,   4,   20,  56,  0,    5,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    
    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print()
    
while True:
    t = rtc.datetime
    #print(t)     # uncomment for debugging

    print("The date is %s %d/%d/%d" % (days[t.tm_wday], t.tm_mday, t.tm_mon, t.tm_year))
    print("The time is %d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec))
    
    time.sleep(1) # wait a second