import os

def set_nonblock(fobj):
    try:
        setblocking = fobj.setblocking
    except AttributeError:
        try:
            import fcntl
        except ImportError:
            raise NotImplementedError
        try:
            fd = fobj.fileno()
        except AttributeError:
            fd = fobj
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    else:
        setblocking(False)
