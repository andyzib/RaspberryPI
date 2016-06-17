#!/usr/bin/python3
#from picamera import PiCamera
import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)

# Some constants to help make readable code. 
BUTTON_NEXT = 26  # Next button, GPIO 26
BUTTON_BACK = 16  # Back button, GPIO 16
BUTTON_START = 21 # Start Button, GPIO 21

# Number of Photos to Take
NUMPHOTOS = 4

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
# List of effects to cycle through.
globalEffectList = ['none','sketch','posterise','emboss','negative','colorswap',
                    'hatch','watercolor','cartoon','washedout','solarize','oilpaint']
# List of friendly names for the various effects.
globalEffectDict = {'none': 'Normal','sketch':'Artist Sketch','posterise':'Poster','emboss':'Embossed',
                    'negative':'Negative Zone','colorswap':'Swap Colors','hatch':'Crosshatch','watercolor':'Water Color',
                    'cartoon':'Cartoon','washedout':'Washed Out','solarize':'Solar Flare','oilpaint':'Oil Painting'}
# Set the current effect.
# Current effect.
globalEffectCurr = 0
# Number of effects.
globalEffectLeng = len(globalEffectList)-1

# Photobooth SessionID
SessionID = 0

# Working Directory
globalWorkDir = '/home/aszbikowski/PhotoBooth_WorkDir'
# Session Directory
globalSessionDir = ''

camera = picamera.PiCamera()
camera.rotation = 180
camera.framerate = 15
# Default text size is 32, range is 6-160.
camera.annotate_text_size = 96

# Set Camera Annotation Text.
def SetAnnotate(aText):
    #camera.annotate_background('Blue')
    #camera.annotate_foreground('Yellow')
    camera.annotate_text = aText
# End function. 

# Function to change effect.
def SetEffect(NewEffect):
    global globalEffectList
    global globalEffectCurr
    global camera
    print('Switching to effect ' + NewEffect)
    camera.image_effect = NewEffect
    SetAnnotate("Effect: %s" % globalEffectDict[NewEffect])
    #sleep(10)
    #SetAnnotate("")
# End of function.

# Function to cycle effects forward. 
def NextEffect( ):
    global globalEffectList
    global globalEffectCurr
    if SessionID != 0:
        return False
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
    if SessionID != 0:
        return False
    if globalEffectCurr == 0:
        globalEffectCurr = globalEffectLeng
    else:
        globalEffectCurr = globalEffectCurr - 1
    NextEff = globalEffectList[globalEffectCurr]
    SetEffect(NextEff)
    return True
# End of Function

def QuitGracefully():
    camera.stop_preview()
    camera.close()
    GPIO.remove_event_detect(BUTTON_NEXT)
    GPIO.remove_event_detect(BUTTON_BACK)
    GPIO.remove_event_detect(BUTTON_START)
    GPIO.cleanup()
    quit("Quitting program gracefully.")
# End of function

# Generates a PhotoBoot Session
def SetupPhotoboothSession():
    global SessionID
    global globalWorkDir
    global globalSessionDir
    SessionID = time.time() # Use UNIX epoc time as session ID.
    # Create the Session Directory for storing photos.
    globalSessionDir = globalWorkDir + '/' + str(SessionID)
    os.makedirs(globalSessionDir, exist_ok=True)
# End of function

def TakePhoto( PhotoNum ):
    global SessionID
    global globalSessionDir
    PhotoPath = globalSessionDir + '/' + str(PhotoNum) + '.jpg'
    SetAnnotate('')
    camera.capture(PhotoPath)
# End of function

def RunCountdown():
    SetAnnotate('3')
    sleep(1)
    SetAnnotate('2')
    sleep(1)
    SetAnnotate('1')
    sleep(1)
    SetAnnotate('CHEESE!!!')
    sleep(1)

def ResetPhotoboothSession():
    global SessionID
    SessionID = 0
# End of function

def RunPhotoboothSession():
    global NUMPHOTOS
    remaingPhotos = NUMPHOTOS
    SetupPhotoboothSession()
    while remaingPhotos > 0:
        RunCountdown()
        TakePhoto(remaingPhotos)
        remaingPhotos = remaingPhotos -1
    ResetPhotoboothSession()
# End of function.

def callback_button_press(input_pin):
    if (input_pin == BUTTON_NEXT):
        print("NEXT button pressed!")
        NextEffect()
    elif (input_pin == BUTTON_BACK):
        print("BACK button pressed!")
        PrevEffect()
    elif (input_pin == BUTTON_START):
        print("START button pressed!")
        RunPhotoboothSession()
        QuitGracefully()
    else:
        print("Unknown button pressed!")
# End of function.

# Define GPIO button press interrupts.
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
