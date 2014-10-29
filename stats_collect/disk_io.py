# encoding: utf-8

import time
import psutil


def calc_delta(prev, current):
    return dict([
        (f, (getattr(current, f) - getattr(prev, f)))
        for f in current._fields
    ])


def calc_speed(delta, ts):
    return dict([
        (k, v/ts) for k, v in delta.iteritems()
    ])


class DiskIOStats(object):

    def __init__(self):
        self.last_req_time = None
        self.prev = None
        self.speed = {}

    def update(self):
        ts = time.time()
        data = psutil.disk_io_counters()
        if self.last_req_time:
            delta = calc_delta(self.prev, data)
            self.speed = calc_speed(delta, ts - self.last_req_time)
        self.prev = data
        self.last_req_time = ts

    def get_metric(self):
        return self.speed

    def as_influxdb(self):
        self.update()
        if self.speed:
            return {'name': 'disk_io',
                    'columns': self.speed.keys(),
                    'points': self.speed.values()}
        return {}
