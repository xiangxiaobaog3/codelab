# encoding: utf-8

import csv

D = {'name': u'你是谁', 'welcome': u'问候你'}

with open('out.csv', 'wb') as fb:
    fb.write(u'\ufeff'.encode('utf8')) # BOM (optional ... Excel needs it to open UTF-8 file properly)
    w = csv.DictWriter(fb, sorted(D.keys()))
    w.writeheaders()
    w.writerow({k: v.encode('utf8') for k, v in D.items()})

# coding: utf-8
import csv
import cStringIO
import codecs

class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()

D1 = {'name':u'马克','pinyin':u'Mǎkè'}
D2 = {'name':u'美国','pinyin':u'Měiguó'}
f = open('out.csv','wb')
f.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
w = DictUnicodeWriter(f,sorted(D.keys()))
w.writeheader()
w.writerows([D1,D2])
f.close()
