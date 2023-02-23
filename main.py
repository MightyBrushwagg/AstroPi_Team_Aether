from pathlib import Path
from datetime import datetime, timedelta
from time import sleep
from picamera import PiCamera
from orbit import ISS, ephemeris
from skyfield.api import load
from logzero import logfile, logger

###TEAM AETHER###
"""
    Check if sunlit
    If there is sunlight then take picture
    store it in folder aether pictures
    once we have images we can convert them to ndvi on earth
"""

def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (positive rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    ###from astropi guide ###
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle



def capture(camera, image):
    ### from astropi guide ###
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    point = ISS.coordinates()

    ## Convert the latitude and longitude to EXIF-appropriate representations ##
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    ## Set the EXIF tags specifying the current location ##
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    ## Capture the image ##
    camera.capture(image)

## locate current directory and initiate image folder directory variable ##

### from astropi guides ###
base_folder = Path(__file__).parent.resolve() 

image_directory  = f"{base_folder}/aether_pictures"

logfile(base_folder/"events.log", maxBytes=1e3, backupCount=1)

## initiate camera ##
camera = PiCamera()


## counter to name images uniquely ##
counter = 0


### Code copied from astropi guides ###
## Create a `datetime` variable to store the start time ##
start_time = datetime.now()
## Create a `datetime` variable to store the current time ##
## (these will be almost the same at the start) ##
now_time = datetime.now()
## Run a loop for just under 3 hours ##
while (now_time < start_time + timedelta(minutes=178)):
    try:
        ## twelve second delay
        sleep(12)
        
        ## checking if ISS is sunlit ##
        timescale = load.timescale()
        t = timescale.now()
        if ISS.at(t).is_sunlit(ephemeris):

            ## take picture with metadata during the day and increase counter ##
            capture(camera, f"{image_directory}/aether_image{counter}.jpg")
            counter += 1
            
       
        ## Update the current time and counter ##
        now_time = datetime.now()

    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        ## If error is picture folder not existing then create one. Though there should be one in the zip file alongside the python file
        if e.__class__.__name__ == "FileNotFoundError":
            pictures_folder = base_folder/"aether_pictures"
            pictures_folder.mkdir()


### CLOSE THE CAMERA & PROGRAM ###
camera.close()
quit()
