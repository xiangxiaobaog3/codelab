#!/usr/bin/env python
# encoding: utf-8

import requests
from bs4 import BeautifulSoup

"""
This site brings you science-based answers and expert insight on how
to be awesome at life.
"""


url = 'http://www.bakadesuyo.com/blog/'
r = requests.get(url)
soup = BeautifulSoup(r.content)

tags = soup.find_all(class_="post_details")
for tag in tags:
    sub_tag = tag.find("a")
    href = sub_tag.attrs['href']
    print(u"{0}, {1}".format(sub_tag.text, href))
