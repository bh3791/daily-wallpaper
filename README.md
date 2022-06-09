# Wallpaper of the Day

This is a simple Python 3.9 script for macOS Big Sur and above. It downloads 
a NASA or Bing image of the day from the appropriate RSS feed, and sets it 
as the desktop wallpaper. It also creates a notification center popup describing 
the image.

## Usage
Running is as simple as:

    python wallpaper.py

Although of course you may in practice want to specify the path to the script.

## Scheduling
It can be scheduled using crontab as follows, at the command line:

    crontab -e

then, enter the following data to run it at 9am each day:

    0 9 * * * ~/venv/bin/python ~/Documents/GitHub/daily-wallpaper/wallpaper.py

This example uses a virtual environment. But you can specify whatever python you like as long as it uses python 3.9 or above. For more help with cron, check out https://crontab.guru/
