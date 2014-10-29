#!/usr/bin/env python
# encoding: utf-8

import time

import psutil
import influxdb

host = 'localhost'
port = 8086
username = 'root'
password = 'root'
database = 'rocks'


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
        self.update()

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
        return {'name': 'disk_io',
                'columns': self.speed.keys(),
                'points': self.speed.values()}


class NetIOCounter(object):
    def __init__(self):
        self.last_req = None
        self.last_req_time = 0
        self.perinc = True
        self.include_interface = [
            'eth0',
        ]

    def _get_net_io_counters(self):
        counters = psutil.net_io_counters(self.perinc)
        res = {}
        for name, io in counters.iteritems():
            res[name] = io._asdict()
            res[name].update({'tx_per_sec': 0, 'rx_per_sec': 0})
        return res

    def _set_last_req(self, counters):
        self.last_req = counters
        self.last_req_time = time.time()

    def _get(self):
        return self.last_req

    def update(self):
        counters = self._get_net_io_counters()

        if not self.last_req:
            self._set_last_req(counters)
            return counters

        time_delta = time.time() - self.last_req_time

        for name, io in counters.iteritems():
            last_io = self.last_req.get(name)

            if not last_io:
                continue
            tx_per_sec = (io['bytes_sent'] - last_io['bytes_sent']) / time_delta
            rx_per_sec = (io['bytes_recv'] - last_io['bytes_recv']) / time_delta
            io.update({'tx_per_sec': tx_per_sec, 'rx_per_sec': rx_per_sec})

        self._set_last_req(counters)
        return counters

    def get(self):
        self.update()
        counters = self._get()

        d = []
        for name, io in counters.iteritems():

            if name not in self.include_interface:
                continue

            d.append({'name': 'network.%s' % name, 'columns': io.keys(), 'points': [io.values()]})
        return d

def get_cpu():
    d = psutil.cpu_times_percent()._asdict()
    return {'name': 'cpu_times', 'columns': d.keys(), 'points': [d.values()]}

def get_process():
    procs = []
    for p in psutil.process_iter():
        procs.append(p.as_dict(['username', 'get_nice', 'get_memory_info',
                                'get_memory_percent', 'get_cpu_percent',
                                'get_cpu_times', 'name', 'status']))


def get_memory():
    d = psutil.virtual_memory()._asdict()
    return {'name': 'memory', 'columns': d.keys(), 'points': [d.values()]}

def get_swap_memory():
    d = psutil.swap_memory()._asdict()
    return {'name': 'swap_memory', 'columns': d.keys(), 'points': [d.values()]}

def get_disk_io():
    d = psutil.disk_io_counters()._asdict()
    return {'name': 'disk_io', 'columns': d.keys(), 'points': [d.values()]}

def get_disk_usage():
    partitions = psutil.disk_partitions()
    data = {'name': 'disk_io', 'columns': [], 'points': []}
    for partition in partitions:
        d = psutil.disk_usage(partition.mountpoint)._asdict()
        if not data['columns']:
            data['columns'] = ['partition'] + d.keys()
        data['points'].append([partition.mountpoint] + d.values())
    return data


def main():
    db = influxdb.InfluxDBClient(host, port, username, password, database)
    # print(data)
    nio = NetIOCounter()
    dio = DiskIOStats()
    while True:
        data = [
            get_cpu(),
            get_disk_usage(),
            get_disk_io(),
            get_memory(),
            get_swap_memory(),
            dio.as_influxdb(),
        ] + nio.get()
        db.write_points(data)
        print('-->')
        time.sleep(10)

if __name__ == '__main__':
    main()
