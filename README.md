## Status

This project is still in development

## Synopsis

Code to go along with Raspberry pi power sprinkler described here <url>

This code contains the script "run_sprinkler.py" which automatically runs an outside sprinkler 
on a fixed schedule using a crontab.  The sprinkler will only run if there has been little to 
no rain in the past 24 hours.  The script uses the Weather Underground API to estimate recent rainfall

## Requirements

This project requires the following:

1.  A free developer API to Weather Underground (we won't be making many requests per day)

https://www.wunderground.com/weather/api/d/pricing.html

Select the "Anvil" plan so you gain access to the most features.  This process should give you an API key that looks
something like a string of numbers and letters, e.g. 3d42bd4e2f42a2eb.

2.  The requests python module. Run these commands to get you what you need:   
```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git
sudo apt-get install python-pip
sudo pip install requests
```

## Setup

Download or clone this repo onto your Raspberry pi.  This command will put the code under your home directory:
```
cd $HOME
git clone https://github.com/markveillette/rpi_sprinkler.git
cd rpi_sprinkler
```
If you install the code somewhere esle remember the location.

If you look in this directory, you'll see two file with a `.sample` extension.  Start by copying or renaming these files to remove the `.sample` extension:
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

## Installation

Finally, to install the crontab, open `run.crontab` and on the last line enter the full path to the script `run_sprinkler.py`.  If you followed the steps above this should already be done for you.  Set the hour(s) you want the sprinker to run at the start of the last line.  By default, it's set to run at 6am and 6pm every day.

To install the cron, run
```
sudo crontab run.crontab
```
Check the log file to monitor how things are going.  Good luck!

















