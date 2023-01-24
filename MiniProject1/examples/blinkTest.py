# Lines with a '#' in front are comments and are not interpreted as code
#
# Written by James Crall, 2023
# Digital Ecology, UW-Madison, Spring 2023

# import necessary python libraries
import board
import digitalio
import time

## Set up led pin
led = digitalio.DigitalInOut(board.LED) #create a variable 
led.direction = digitalio.Direction.OUTPUT #

while True: #This create a loop so that the code runs continuously after it has started
	
	# sections within 'while' and 'for' loops (and functions) in python are indented
    led.value = True #Turn the LED on
    time.sleep(2) #Delay two seconds
    led.value = False #Turn the LED off
    time.sleep(2) #delay two seconds
    
    print('success!') #Confirm this worked by printing to the serial port
