import os
import sys
from time import sleep
from contextlib import contextmanager

fn = '/tmp/lock_file_test.lock'

def test_with_os():
    try:
        fd = os.open(fn, os.O_WRONLY | os.O_CREAT | getattr(os, 'O_BINARY', 0) | os.O_EXCL)
        print fd
        os.write(fd, str(os.getpid()))
        sleep(11111)
        os.close(fd)
    except OSError:
        print 'lock file existed'
    finally:
        os.unlink(fn)

@contextmanager
def test_with_statement(lock_file):
    if os.path.exists(lock_file):
        print 'Only one script can run at once. lock file: %s' % lock_file
        sys.exit(-1)
    else:
        fb = open(lock_file, 'wb')
        fb.write(str(os.getpid()))
        try:
            yield
        finally:
            os.unlink(lock_file)

with test_with_statement(fn):
    print 'doing'
    sleep(2)
