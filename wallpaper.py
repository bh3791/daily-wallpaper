import os
import subprocess
from time import strftime
import requests
from xml.dom.minidom import parseString

# Defines source and destination of image
rss_feed_bing = 'https://www.bing.com/HPImageArchive.aspx?format=rss&idx=0&n=1&mkt=en-US'
rss_feed_nasa = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'

rss_feed = rss_feed_nasa
is_bing = (rss_feed_bing is rss_feed)

os.makedirs('~/Pictures/DeskFeed', exist_ok=True)
dst_dir = os.path.expanduser('~/Pictures/DeskFeed/')

SCRIPT0 = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "{0}"
end tell
END"""

SCRIPT1 = """/usr/bin/osascript<<END
display notification "{0}" with title "Picture of the Day"
END"""


def set_desktop_background(destination, desc):
    script0 = SCRIPT0.format(destination)
    subprocess.Popen(script0, shell=True)

    script1 = SCRIPT1.format(desc)
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

    if is_bing:
        first_item = dom.getElementsByTagName('item')[0]
        link = "https://bing.com" + first_item.getElementsByTagName('link')[0].firstChild.data
        desc = first_item.getElementsByTagName('title')[0].firstChild.data
    else:
        first_item = dom.getElementsByTagName('item')[0]
        link = first_item.getElementsByTagName('enclosure')[0].getAttribute('url')
        desc = first_item.getElementsByTagName('description')[0].firstChild.data

    print(f"getting picture of the day: {link}\n{desc}")

    if os.path.isfile(destination):
        os.unlink(destination)

    try:
        with requests.get(link) as image:
            with open(destination, 'wb') as out:
                out.write(image.content)
    except Exception as e:
        print("Failed to download file caused by {0}".format(e))
        # A existence of an incomplete files prevents its re-download and
        # its usage is not desired hence we have to delete them.
        os.unlink(destination)

    set_desktop_background(destination, desc)


def main():
    parse_feed(rss_feed)


if __name__ == "__main__":
    main()