## Synopsis

Code to go along with the [Raspberry Pi Controlled Irrigation System](http://www.instructables.com/id/Raspberry-Pi-Controlled-Irrigation-System) Instructable by Ben Finio.

This code contains the script "run_sprinkler.py" which automatically runs an outside sprinkler 
on a fixed schedule using a crontab.  The sprinkler will only run if there has been little to 
no rain in the past 24 hours.  The script uses the Weather Underground API to estimate recent rainfall

## Requirements

This project requires a free developer API key to Weather Underground.  Go here to register for one:

https://www.wunderground.com/weather/api/d/pricing.html

Select the "Anvil" plan so you gain access to the most features.  This process should give you an API key that looks
something like a string of numbers and letters, e.g. 3d42bd4e2f42a2eb.

You'll also need the requests python module. These commands will get everything you'll need:   
```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git
sudo apt-get install python-pip
sudo pip install requests
```

## Setup

Download or clone this repo onto your Raspberry pi.  These commands will put a `rpi_sprinkler` directory containing code under your home directory:
```
cd $HOME
git clone https://github.com/markveillette/rpi_sprinkler.git
cd rpi_sprinkler
```
If you install the code somewhere else keep track of the location for the crontab file.

If you look in this directory, you'll see two files with a `.sample` extension.  Start by copying or renaming these files to remove the `.sample` extension:
```
cp config.sample config
cp run.crontab.sample run.crontab
```

Open `config` with your favorite text editor (nano, vim, emacs, etc..) and fill in your information to the right of each equal sign.  This is where you will paste the API key you obtained from Weather Underground above.

## Testing

Before installing the crontab, it's probably a good idea to test the APi is working. To do so, run 
```
python run_sprinkler.py test
```
If you see a message like 
```
API seems to be working with today's rainfall=0.000000 and past 24 hour rainfall=0.020000
```
everything is going okay.  If you see some other message, check the internet connection, the API key, and the info you entered in the `config` file.

To run the sprinkler (assuming it's hooked up), run
```
sudo python run_sprinkler.py force
```
This should run the sprinkler without checking if it rained.  It will also make a note in the log file (specified in the `config` file).  If this doesn't work, check the GPIO pin in `config` is correct.

## Installing the crontab

Now that the script is working, the final step is to install a crontab so that `run_sprinkler.py` runs on a fixed schedule.  A crontab (or cron for short) is a simple text file that is used by Linux to run tasks at specified times.  We'll be setting a cron to execute the script run_sprinkler.py.

To setup the crontab, open `run.crontab` with your favorite text editor.  The basic format of the crontab file is as follows (lines begining with "`#`" are comments):

```
# minute   hour    day of month   month    weekday      Command    
# (0-59)  (0-23)    (1-31)       (1-12)     (0-6)                
    *        *        *           *           *         command
```

Decide what schedule you'd like to set and replace the approprite asteriks * with the weekdays,hours,minutes, etc you'd like.  For example, to execute run_sprinkler.py every day at 6am and 6pm, `run.crontab` should look like this:

```
# minute   hour    day of month   month    weekday      Command    
# (0-59)  (0-23)    (1-31)       (1-12)     (0-6)                
    0      6,18        *             *         *        /usr/bin/python2.7 /home/pi/rpi_sprinkler/run_sprinkler.py
```

Where the "6,18" in the hour column and *'s everywhere else means to run at 6:00 and 18:00 local time every day.  Notice that we included the full paths to both python2.7 and the run_sprinkler.py script (if you have the script in a different location make sure to modify the path).  The Linux environment in which a crontab runs is typically very minimal, so it's safe not to assume anything about your $PATH or other environment variables.

This example will run at 12pm every Monday, Wednesday and Friday:
```
# minute   hour    day of month   month    weekday      Command    
# (0-59)  (0-23)    (1-31)       (1-12)     (0-6)                
    0      12         *             *       1,3,5       /usr/bin/python2.7 /home/pi/rpi_sprinkler/run_sprinkler.py
```

This will run at 6pm every second day:
```
# minute   hour    day of month   month    weekday      Command    
# (0-59)  (0-23)    (1-31)       (1-12)     (0-6)                
    0      18        */2           *         *       /usr/bin/python2.7 /home/pi/rpi_sprinkler/run_sprinkler.py
```
Google "crontab examples" for more.  

Once you're set up the run.crontab file, install the crontab by entering
```
sudo crontab run.crontab
```
and you should be all set.  Check the log file every now and then to monitor how things are going.  

UPDATE (5/14/16):  I added a @reboot command on the last line of the crontab file that sets all GPIO pins used to GPIO.LOW when the pi restarts.  This was done to make sure the sprinkler doesn't run spontaneously if the pi accidentally reboots.  If you installed rpi_sprinker in a different spot, make sure the path to `run_sprinkler.py` matches on this line as well.

If you restart the raspberry pi, the crontab should restart with it.  To check if it's running, enter
```
sudo crontab -l
```
and you should see the contents of `run.crontab` appear.  If you see nothing, you'll need to reinstall the crontab.  If you ever want to remove the crontab, enter `sudo crontab -r`.

Good luck!

