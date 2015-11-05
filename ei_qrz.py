#!/usr/bin/python

"""
    ei_qrz.py
    --all : list all entries in EI callbook.
    --search : search EI callbook for string.
    --url : provide an alternative URL
"""

import urllib2
import re
import sys
import argparse

class CallBook(object):
    """
    Callbook Class
    """
    def __init__(self, url):
        self.url = url
        self.ei_callbook = []
        self.request_header = {'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    def get_callbook(self):
        """
        Grab the current EI online callbook
        Clean up the data
        Put the data into a list
        Headers have to be set to pull page from IRTS web-site otherwise 403s returned.
        """
        self.request = urllib2.Request(self.url, headers=self.request_header)
        self.response = urllib2.urlopen(self.request)
        self.the_page = self.response.readlines()
        for self.call in self.the_page:
            self.match = re.search(r'<tr><td><b>EI', self.call)
            if self.match:
                self.call_clean1 = re.sub(r'<tr><td><b>', '', self.call)
                self.call_clean2 = re.sub(r'</b></td><td>', ':', self.call_clean1)
                self.call_clean3 = re.sub(r'</td></tr>', '', self.call_clean2)
                self.call_clean4 = re.sub('\n', '', self.call_clean3)
                self.ei_callbook.append(self.call_clean4)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--search",
        help="String to search",
        type=str)

    parser.add_argument(
        "--all",
        action="store_true",
        help="Display all callbook entries")

    parser.add_argument(
        "--url",
        help="EI Callbook URL",
        default="http://www.irts.ie/callbook/index.html",
        type=str)

    args = parser.parse_args()

    try:
        if args.all:
            callbook = CallBook(args.url)
            callbook.get_callbook()
            for qrz in callbook.ei_callbook:
                print qrz
        elif args.search:
            callbook = CallBook(args.url)
            callbook.get_callbook()
            for qrz in callbook.ei_callbook: 
                if re.findall(args.search.lower(), qrz.lower()):
                    print qrz
        else:
            print("Nothing to do.")

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception, e:
        str(e)
        print("Computer says: {}").format(e)

