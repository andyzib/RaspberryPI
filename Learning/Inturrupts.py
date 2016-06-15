#!/usr/bin/python3
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Some constants to help make readable code. 
BUTTON_NEXT = 26
BUTTON_BACK = 16
BUTTON_START = 21

#from gpiozero import Button
#button = Button(26)

# Next Button, GPIO 26
GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Prev Button, GPIO 16
GPIO.setup(BUTTON_BACK, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Start button, GPIO 21
GPIO.setup(BUTTON_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def callback_button_press(input_pin):
    if (input_pin == BUTTON_NEXT):
        print("NEXT button pressed!")
    elif (input_pin == BUTTON_BACK):
        print("BACK button pressed!")
    elif (input_pin == BUTTON_START):
        print("START button pressed!")
        quit()
    else:
        print("Unknown button pressed!")

GPIO.add_event_detect(BUTTON_NEXT, GPIO.FALLING, callback=callback_button_press, bouncetime=300)
GPIO.add_event_detect(BUTTON_BACK, GPIO.FALLING, callback=callback_button_press, bouncetime=300)
GPIO.add_event_detect(BUTTON_START, GPIO.FALLING, callback=callback_button_press, bouncetime=300)

try:
    print("Nothing to do yet.")
    while True:
        sleep(1)
        # Do nothing. Infinite loop!
    print("Still nothing to do.")
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
