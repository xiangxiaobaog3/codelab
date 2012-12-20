#!/usr/bin/env python
# encoding: utf-8

import json
from urllib import urlencode
from urllib2 import urlopen

location_code = "CHXX0037"
large_image = "http://l.yimg.com/os/mit/media/m/weather/images/icons/l/%(code)sd-100567.png"
img_path = '/tmp/weather.png'
query = urlencode({'q': "select location, item from weather.forecast where location='%s' and u='c'" % location_code,
                   'format': 'json',
                   'lang': 'zh-CN'})

weather_api = 'http://query.yahooapis.com/v1/public/yql?' + query

def open_url(url):
    # print url
    resp = None
    try:
        resp = urlopen(url)
        return resp.read()
    except IOError, e:
        print e
    return resp

def main():
    weather_data = open_url(weather_api)
    if weather_data is not None:
        data = json.loads(weather_data)
        # count = data['query']['count']
        channel = data['query']['results']['channel']
        location = channel['location']['city']
        item = channel['item']
        code = item['condition']['code']
        temp = item['condition']['temp']
        text = item['forecast'][0]['text']
        output = u'%s°C\n%s\n%s' % (temp, text, location)
        print output.encode('utf8')
        large_image_url = large_image % {'code': code}
        img = open_url(large_image_url)
        if img is not None:
            with open(img_path, 'wb') as fb:
                fb.write(img)

if __name__ == "__main__":
    main()
