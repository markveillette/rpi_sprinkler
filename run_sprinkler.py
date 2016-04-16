import os
import requests
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
GPIO.setmode(GPIO.BCM)

#### YOU NEED TO SET THE FOLLOWING VARIABLES:
# Set these for wherever you live
TOWN  = 'Wilmington'
STATE = 'MA'

# What is the daily threshold for running the sprinkler?
RAIN_THRESHOLD_IN = 0.05

# How long should the sprinkler run at a time in minutes?
RUNTIME_MIN = 1

# What GPIO will send the +5V?
GPIO_PIN = 23

# API key I got from weather underground
API_KEY = '9d71ab4d7e91b7fb'

# URL used for the field we want
API_URL = 'http://api.wunderground.com/api/{key}/conditions/q/{state}/{town}.json'

# Name of a log file to print progress
# Set this to None if you don't want a log file
LOG_FILE = '/home/pi/projects/sprinkler/sprinkler.log'
#######################

# Method to access wu API and return the "precip_today_in" field 
def get_precip_today_in():
  r = requests.get(API_URL.format(key=API_KEY,state=STATE,town=TOWN))
  rainfall = None
  if r.ok:
    try:  
      rainfall = float(r.json()['current_observation']['precip_today_in'])
    except Exception as ex:
      rainfall = None
  return rainfall,r

def run():
  try:
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN, GPIO.HIGH )
    sleep( RUNTIME_MIN * 60 ) 
    GPIO.output(GPIO_PIN, GPIO.LOW )
  except Exception as ex:
    GPIO.output(GPIO_PIN, GPIO.LOW )
  GPIO.cleanup()

# Main method
def main():
  # Open log file
  with open(LOG_FILE,'a') as log_file:
    # Current time
    current_time = datetime.now().isoformat()
    
    # Get today's rainfall
    rainfall,r = get_precip_today_in()
    if rainfall is None:
      log_file.write('%s: Error getting rainfall amount, setting to 0.0 in\n' % current_time)
      log_file.write('%s: Response text: %s' % (current_time,r.text))
      rainfall = 0.0
    else:
      log_file.write('%s: Rainfall: %f in\n' % (current_time,rainfall))
    
    # If this is less than RAIN_THRESHOLD_IN run sprinkler
    if rainfall <= RAIN_THRESHOLD_IN:
      log_file.write('%s: Starting sprinkler')
      run()
      log_file.write('%s: Stopping sprinkler')
      
if __name__ == "__main__":
    main()
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
     










