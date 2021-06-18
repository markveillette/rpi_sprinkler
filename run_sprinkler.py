import calendar
import configparser
import datetime
import json
import os
import requests
import sys

from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Loads configuration file
def load_config(filename='config'):
  config = configparser.RawConfigParser()
  this_dir = os.path.abspath(os.path.dirname(__file__))
  config.read(this_dir + '/' + filename)
  if config.has_section('SprinklerConfig'):
      return {name:val for (name, val) in config.items('SprinklerConfig')}
  else:
      print('Unable to read file %s with section SprinklerConfig' % filename)
      print('Make sure a file named config lies in the directory %s' % this_dir)
      raise Exception('Unable to find config file')


# Calls open weather history api
def get_weather_history(config, timestamp_dt):
    API_URL = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={day}&appid={key}'
    weather_history = requests.get(API_URL.format(key=config['api_key'],
                                       day=timestamp_dt,
                                       lat=config['lat'],
                                       lon=config['lon']))
    weather_data = json.loads(weather_history.content.decode('utf-8'))
    hourly_rain = {x.get('dt'): x.get('rain').get('1h') for x in weather_data.get('hourly') if x.get('rain') and x.get('dt') >= timestamp_dt}
    return hourly_rain

def get_weather(config, timestamp_dt):
    API_URL = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&dt={day}&appid={key}'
    weather_today = requests.get(API_URL.format(key=config['api_key'],
                                       day=timestamp_dt,
                                       lat=config['lat'],
                                       lon=config['lon']))
    weather_data = json.loads(weather_today.content.decode('utf-8'))
    curr_rain = {}  
    curr = weather_data.get('current')

    if curr:
      rain = curr.get('rain', 0)
      if rain:
        curr_rain = {timestamp_dt: rain.get('1h', 0)}

    hourly_rain = {x.get('dt'): x.get('rain').get('1h') for x in weather_data.get('hourly') if x.get('rain') and x.get('dt') < timestamp_dt}
    hourly_rain.update(curr_rain)
    return hourly_rain

# Gets recent rainfall using open weather API
# By default estimates rainfall in past 24 hours
# to get something different use a different time_win
# (Note this doesn't go further back than yesterday)
def get_precip_in_window(config, time_win_hr=24):
    # Get the utc date from yesterday and convert to Unix timestamp
    yesterday_timestamp = calendar.timegm((
      datetime.datetime.utcnow() - \
      datetime.timedelta(hours=time_win_hr)).utctimetuple())
    # Get the utc date from today and convert to Unix timestamp
    today_timestamp = calendar.timegm(
      datetime.datetime.utcnow().utctimetuple())

    
    # Get observations for today and yesterday
    try:
        hourly_rain_yest = get_weather_history(config, yesterday_timestamp)
    except Exception as ex: 
        print(ex)
        return None
    try:
        hourly_rain_today = get_weather(config, today_timestamp)
    except Exception as ex:
        print(ex)
        return None
   
    try: 
        total = 0   

        # Combine the dictionaries based on timestamp values
        # to eliminate possible duplicates
        hourly_rain_yest.update(hourly_rain_today)
        total += sum(hourly_rain_yest.values())
    except Exception as ex:
        pass
    return total

# Runs sprinkler
def run_sprinkler(config):
  pin = int(config['gpio_starter'])
  led = int(config['gpio_led1'])
  runtime = float(config['runtime_min'])
  with open(config['log_file'],'a') as log_file:
    try:
      GPIO.setup((pin, led), GPIO.OUT)
      log_file.write('%s: Starting sprinkler\n' % datetime.datetime.now())
      GPIO.output((pin,led), GPIO.HIGH)
      sleep(runtime * 60) 
      log_file.write('%s: Stopping sprinkler\n' % datetime.datetime.now())
      GPIO.output((pin,led), GPIO.LOW)
    except Exception as ex:
      log_file.write('%s: An error has occurred: %s \n' % (datetime.datetime.now(), ex.message))  
      GPIO.output((pin,led), GPIO.LOW)

# Main method
#   1.  Reads config file
#   2.  Checks past 24 hours of rainfall
#   3.  Runs sprinkler if rainfall falls below threshold
def main(): 
  # Load configuration file  
  config = load_config()
    
  with open(config['log_file'],'a') as log_file:
    # Get past 24 hour precip
    rainfall = get_precip_in_window(config)
    if rainfall is None:
      log_file.write('%s: Error getting rainfall amount, setting to 0.0 mm\n' % datetime.datetime.now())
      rainfall = 0.0
    else:
      log_file.write('%s: Rainfall: %f in\n' % (datetime.datetime.now(), rainfall))
    
  # If this is less than rain_threshold_mm run sprinkler
  if rainfall <= float(config['rain_threshold_mm']):
    run_sprinkler(config)

# Test API access
def test_api():
  config = load_config()
  total = get_precip_in_window(config)

  if total is None:
    print("API works but unable to get history.  Did you sign up for the right plan?")
    return
    
  print("API seems to be working with past 24 hour rainfall=%f" % (total))  
    
# Runs without checking rainfall
def force_run():
  config = load_config()
  run_sprinkler(config)
  
# Sets all GPIO pins to GPIO.LOW.  Should be run when the 
# raspberry pi starts.
def init():
    config = load_config()
    pin = int(config['gpio_starter'])
    led = int(config['gpio_led1'])
    GPIO.setup((pin, led), GPIO.OUT)
    GPIO.output((pin,led), GPIO.LOW)      
    
if __name__ == "__main__":
  if len(sys.argv) == 1:
    # Standard mode
    main()
  elif len(sys.argv) == 2 and sys.argv[1] == 'test':
    # Tests connection to API
    # Make sure you run as root or this won't work
    test_api()
  elif len(sys.argv) == 2 and sys.argv[1] == 'force':
    # Runs sprinkler regardless of rainfall
    force_run()
  elif len(sys.argv) == 2 and sys.argv[1] == 'init':
    # Sets pin and led GPIOs to GPIO.LOW
    init()
  else:
    print("Unknown inputs", sys.argv)
        
        
    
    
    
    
