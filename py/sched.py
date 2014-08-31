# encoding: utf-8

import datetime
import schedule
import time

def job(n):
    print datetime.datetime.now()
    print("I'm working ...", n)

j = schedule.every(10).seconds.do(job, n='every 10 seconds')
schedule.every(1).minute.do(job, n='every 1 minute')
schedule.every().day.at("11:08").do(job, n='11:08')

while True:
    schedule.run_pending()
    time.sleep(1)

