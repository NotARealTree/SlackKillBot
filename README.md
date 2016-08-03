# Slack Kill Bot

A small python script that, in cooperation with a bot you make on slack, will post your corporations' kills to a channel of your choosing.
The types are up to date for the **Aegis** release, I'll try to keep it up to date. 

## Setup

1. Clone this repo, or just download kills.py and the sample config file.
2. Either manually install [requests](http://www.python-requests.org/en/latest/) and [slackclient](https://github.com/slackhq/python-slackclient) or use pip-install requirements.txt tp install the requirements in one go.
3. Fill out the config file with your relevant info.
4. Set up a [cronjob](http://askubuntu.com/questions/2368/how-do-i-set-up-a-cron-job) or similar for your system, set to run kills.py at the same intervals as you have specified in the config file.

## Config

Given that the config has comments explaining it I won't go into too much detail here. I will however state a few things.

- You can get your corporation ID from [dotlan](http://evemaps.dotlan.net/) by searching for the corporation name.
- In its current form, this will not work for alliances, feel free to modify it accordingly and under the terms of the license.
- You can set the frequency at which you'd like to refresh. Don't set this too low. If you spam zKillboard with requests through this, odds are they will contact me (unless you changed the user_agent in the config) before blacklisting the IP (they might not, who knows), given that my name is in the header. If that happens I'll have no idea who you are so there's nothing I can really do.


## License

This code is provided under the **MIT License**, a copy of which can be found in this repository.

## Roll Credits

- Thanks to the guys who made the requests library and the slackclient library, they are both most excellent and easy to use.
- Thanks also to Steve Ronukens [fuzzwork](https://www.fuzzwork.co.uk/) for the static data export of eve id's.

