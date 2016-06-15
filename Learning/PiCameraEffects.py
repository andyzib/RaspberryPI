#!/usr/bin/python
from picamera import PiCamera
from time import sleep

# All effects available 
globalEffectList = ['none','sketch','posterise','gpen','colorbalance','film','pastel','emboss','denoise','negative','blur','colorswap','colorpoint','saturation','hatch','watercolor','cartoon','deinterlace1','deinterlace2','washedout','solarize','oilpaint']
# Set the current effect. 
globalEffectCurr = 'none'
# Setup iterator. 
globalEffectIter = iter(globalEffectList)

# Function to cycle effects. 
def NextEffect( ):
    NextEff = globalEffectIter.next()
    camera.image_effect = NextEff
    camera.annotate_text = "Effect: %s" % NextEff
# End of function. 

camera = PiCamera()
camera.rotation = 180
camera.framerate = 15
camera.start_preview()

# Max Resolution
#camera.resolution = (2592, 1944)
#sleep(5)
# 1080 monitor
#camera.resolution = (1920, 1080)

# Default text size is 32, range is 6-160.
camera.annotate_text_size = 96

#for effect in camera.IMAGE_EFFECTS:
#    camera.image_effect = effect
#    print(effect)    

for effect in camera.IMAGE_EFFECTS:
#    camera.image_effect = effect
#    camera.annotate_text = "Effect: %s" % effect
    NextEffect()
    sleep(5)

camera.stop_preview()
