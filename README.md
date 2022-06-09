# Wallpaper of the Day

This is a simple Python 3.9 script for Mac Big Sur+. It downloads a NASA or Bing image of the day from the appropriate RSS feed, and sets it as the desktop wallpaper. It can be scheduled using crontab as follows, at the command line:

    crontab -e

then, enter the following data to run it at 9am each day:

    0 9 * * * ~/venv/bin/python ~/Documents/GitHub/daily-wallpaper/wallpaper.py

In this example, I am using a virtual environment. But you can specify whatever path you want for python as long as it uses python 3.9 or above. For more help with cron, check out https://crontab.guru/
