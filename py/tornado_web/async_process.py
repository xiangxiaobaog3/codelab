# encoding: utf-8

import logging
import shlex
import subprocess
import tornado

"""
class ShellHandler(BaseHandler):
    @tornado.web.asynchrounous
    @gen.engine
    def get(self):
        self.write("Before sleep<br />")
        self.flush()
        response = yield gen.Task(call_subprocess, self, "ls /")
        self.write("Output is:\n%s" % (response.read(),))
        self.finish()
"""


def call_subprocess(context, command, callback=None):
    context.ioloop = tornado.ioloop.IOLoop.instance()
    context.pipe = p = subprocess.Popen(shlex.split(command),
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        close_fds=True)
    context.ioloop.add_handler(p.stdout.fileno(),
                               context.async_callback(on_subprocess_result, context, callback),
                               context.ioloop.READ)


def on_subprocess_result(context, callback, fd, result):
    try:
        if callback:
            callback(context.pipe.stdout)
    except Exception, e:
        logging.error(e)
    finally:
        context.ioloop.remove_handler(fd)

