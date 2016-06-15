#!/usr/bin/python
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import LED
from gpiozero import Button

button = Button(26)

ledRED = LED(17)
ledYEL = LED(22)
ledGRN = LED(6)

print('Waiting for button.')
button.wait_for_press()
print('Button pressed!')

# The countdown 

# Three
print('Three - Red!')
ledRED.on()
sleep(1)
ledRED.off()

# Two 
print('Two - Yellow!')
ledYEL.on()
sleep(1)
ledYEL.off()

# One
print('One - Green!') 
ledGRN.on()
sleep(1)
ledGRN.off()

print('Go go go!')
sleep(1)
ledGRN.on()
sleep(1)
ledGRN.off()

sleep(1)
ledGRN.on()
sleep(1)
ledGRN.off()

