#!/usr/bin/python3
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Some constants to help make readable code. 
BUTTON_NEXT = 26  # Next button, GPIO 26
BUTTON_BACK = 16  # Back button, GPIO 16
BUTTON_START = 21 # Start Button, GPIO 21

# Milliseconds for switch bounce time.
# 300 is too fast, 500 is too slow.
# 400 seems about right. 
BOUNCE_TIME = 375

# Setup the GPIO buttons.
### Next Button
GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
### Prev Button, GPIO 16
GPIO.setup(BUTTON_BACK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
### Start button, GPIO 21
GPIO.setup(BUTTON_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# All effects available 
# Everything
## globalEffectList = ['none','sketch','posterise','gpen','colorbalance','film','pastel','emboss','denoise','negative','blur','colorswap','colorpoint','saturation','hatch','watercolor','cartoon','deinterlace1','deinterlace2','washedout','solarize','oilpaint']
# Just the "good" ones?
globalEffectList = ['none','sketch','posterise','emboss','negative','colorswap','hatch','watercolor','cartoon','washedout','solarize','oilpaint']
# Set the current effect. 
globalEffectCurr = 0
globalEffectLeng = len(globalEffectList)-1

camera = PiCamera()
camera.rotation = 180
camera.framerate = 15
# Default text size is 32, range is 6-160.
camera.annotate_text_size = 96

# Set Camera Annotation Text.
def SetAnnotate(aText):
    camera.annotate_text = aText
# End function. 

# Function to change effect.
def SetEffect(NewEffect):
    global globalEffectList
    global globalEffectCurr
    global camera
    print('Switching to effect ' + NewEffect)
    camera.image_effect = NewEffect
    SetAnnotate("Effect: %s" % NewEffect)
    sleep(10)
    SetAnnotate("")
# End of function.

# Function to cycle effects forward. 
def NextEffect( ):
    global globalEffectList
    global globalEffectCurr
    if globalEffectCurr == globalEffectLeng:
        globalEffectCurr = 0
    else:
        globalEffectCurr = globalEffectCurr + 1
    
    NextEff = globalEffectList[globalEffectCurr]    
    SetEffect(NextEff)
# End of function.

# Function to cycle effects backward.
def PrevEffect( ):
    global globalEffectList
    global globalEffectCurr
    if globalEffectCurr == 0:
        globalEffectCurr = globalEffectLeng
    else:
        globalEffectCurr = globalEffectCurr - 1
    NextEff = globalEffectList[globalEffectCurr]
    SetEffect(NextEff)
# End of Function

def callback_button_press(input_pin):
    if (input_pin == BUTTON_NEXT):
        print("NEXT button pressed!")
        NextEffect()
    elif (input_pin == BUTTON_BACK):
        print("BACK button pressed!")
        PrevEffect()
    elif (input_pin == BUTTON_START):
        print("START button pressed!")
        QuitGracefully()
    else:
        print("Unknown button pressed!")
# End of function. 

def QuitGracefully():
    camera.stop_preview()
    GPIO.cleanup()
    quit("Quitting program gracefully.")
# End of function

# Define GPIO button press inturrupts. 
GPIO.add_event_detect(BUTTON_NEXT, GPIO.FALLING, callback=callback_button_press, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(BUTTON_BACK, GPIO.FALLING, callback=callback_button_press, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(BUTTON_START, GPIO.FALLING, callback=callback_button_press, bouncetime=BOUNCE_TIME)

SetEffect('none')
camera.start_preview()

try:
    while True:
        sleep(30)
        # Check status of CUPS maybe? 
except KeyboardInterrupt:
        QuitGracefully()

QuitGracefully()
