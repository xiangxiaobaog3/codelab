# encoding: utf-8

import httplib2
from multiprocessing import Lock, Process, Queue, current_process


def worker(worker_queue, done_queue):
    try:
        for url in iter(worker_queue.get, "STOP"):
            status_code = print_site_status(url)
            done_queue.put("%s - %s got %s." % (current_process().name, url, status_code))
    except Exception, e:
        done_queue.put("%s failed on %s with: %s" % (current_process().name, url, e.message))


def print_site_status(url):
    http = httplib2.Http(timeout=10)
    headers, content = http.request(url)
    return headers.get('status', 'no response')


def main():
    sites = (
        'http://penny-arcade.com/',
        'http://reallifecomics.com/',
        'http://sinfest.net/',
        'http://userfriendly.org/',
        'http://savagechickens.com/',
        'http://xkcd.com/',
        'http://duelinganalogs.com/',
        'http://cad-comic.com/',
        'http://samandfuzzy.com/',
    )

    workers = 2
    worker_queue = Queue()
    done_queue = Queue()
    processes = []

    for url in sites:
        worker_queue.put(url)

    for w in xrange(workers):
        p = Process(target=worker, args=(worker_queue, done_queue))
        p.start()
        processes.append(p)
        worker_queue.put('STOP')


    for p in processes:
        p.join()

    done_queue.put("STOP")

    for status in iter(done_queue.get, 'STOP'):
        print(status)


if __name__ == '__main__':
    main()
