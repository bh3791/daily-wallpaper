import os
import subprocess
from time import strftime
import requests
from xml.dom.minidom import parseString
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-mode', dest='mode', help='The mode to run in, nasa or bing. Nasa is the default', default='nasa')

# Defines source and destination of image
rss_feed_bing = 'https://www.bing.com/HPImageArchive.aspx?format=rss&idx=0&n=1&mkt=en-US'
rss_feed_nasa = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'
web_feed_apod = 'https://apod.nasa.gov/apod/'

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
    # this will fail if you switch from one source to another, as the finder will not update
    # the image if it has the same file name.

    script0 = SCRIPT0.format(destination)
    subprocess.Popen(script0, shell=True)

    script1 = SCRIPT1.format(desc)
    subprocess.Popen(script1, shell=True)


def parse_feed(args):
    if args.mode == 'bing':
        rss = rss_feed_bing
    else:
        rss = rss_feed_nasa

    destination = "%s%s-%s.jpg" % (dst_dir, args.mode, strftime("%y-%m-%d"))

    try:
        rss_contents = requests.get(rss)
    except:
        print(f"Failed to read rss feed {rss}")
        return

    rss_src = rss_contents.content
    dom = parseString(rss_src)

    if args.mode == 'bing':
        first_item = dom.getElementsByTagName('item')[0]
        link = "https://bing.com" + first_item.getElementsByTagName('link')[0].firstChild.data
        desc = first_item.getElementsByTagName('title')[0].firstChild.data
    elif args.mode == 'apod':
        link = load_apod_image()
        desc = "todo: get daily apod description"
    else:
        first_item = dom.getElementsByTagName('item')[0]
        link = first_item.getElementsByTagName('enclosure')[0].getAttribute('url')
        desc = first_item.getElementsByTagName('title')[0].firstChild.data + "\n" + first_item.getElementsByTagName('description')[0].firstChild.data

    print(f"Getting picture of the day: {link}\nTitle: {desc}")

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


def load_apod_image():

    images = []

    res = requests.get(web_feed_apod)
    soup = BeautifulSoup(res.content, 'html.parser')
    items = soup.select('a > img')
    for item in items:
        image_url = web_feed_apod + item.find_parent('a')['href']
        images.insert(0, image_url)
    return images[0]


def main(args):
    parse_feed(args)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)