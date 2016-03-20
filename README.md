## Status

This project is still in development,  check back in the next few months.

## Synopsis

Code used to configure a Raspberry pi to automatically run an outside sprinkler on a fixed schedule.  
The sprinkler will only run if there has been little to no rain in the past 24 hours, 
AND there isn't a high likelihood of rain in the next 24 hours.



## Requirements

This project requires the following:

1.  A free developer API to Weather Underground (we won't be making many requests per day)

https://www.wunderground.com/weather/api/d/pricing.html

I used the Anvil plan.

2.  mysql.  To install run the following (google "install mysql python raspberry pi" for more detailed instructions

Make sure everything is up to date:   
...
sudo apt-get update && sudo apt-get upgrade
...
Install mysql server:   
...
sudo apt-get install mysql-server
...
(follow on screen instructions)

Install python interface:  
...
sudo apt-get install python-mysqldb
...


## Setup

All scripts depend on a configuration file config.pd.

