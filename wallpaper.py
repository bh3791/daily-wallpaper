import os
#import md5
import pprint
import sys
import subprocess
from time import strftime
import requests
from xml.dom.minidom import parseString

# Defines source and destination of image
#rss_feed = 'https://www.bing.com/HPImageArchive.aspx?format=rss&idx=0&n=1&mkt=en-US'
rss_feed = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'
dst_dir = os.path.expanduser('~/Pictures/DeskFeed/')

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "{0}"
end tell
END"""


def set_desktop_background(destination):
    script1 = SCRIPT.format(destination)
    subprocess.Popen(script1, shell=True)


def parse_feed(rss):
    destination = "%s%s.jpg" % (dst_dir, strftime("%y-%m-%d"))
    #if os.path.exists(destination):
    #    sys.exit(0)

    try:
        rss_contents = requests.get(rss)
    except:
        print(f"Failed to read rss feed {rss}")
        return

    rss_src = rss_contents.content
    dom = parseString(rss_src)
    first_item = dom.getElementsByTagName('item')[0]
    link = first_item.getElementsByTagName('enclosure')[0].getAttribute('url')
    desc = first_item.getAttribute('description')
    print(f"downloading picture of the day: {desc}")

    if not os.path.isfile(destination):
        try:
            with requests.get(link) as image:
                with open(destination, 'wb') as out:
                    out.write(image.content)
        except Exception as e:
            print("Failed to download file caused by {0}".format(e))
            # A existence of an incomplete files prevents its re-download and
            # its usage is not desired hence we have to delete them.
            os.unlink(destination)

    set_desktop_background(destination)


def main():
    parse_feed(rss_feed)


if __name__ == "__main__":
    main()