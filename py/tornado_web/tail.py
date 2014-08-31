#!/usr/bin/env python
# encoding: utf-8

import subprocess

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.options
import tornado.web
import tornado.gen

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("inputfile",
       default="test.txt",
       help="the path to the file which we will 'tail'",
       type=str)


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.p = subprocess.Popen(["tail", "-f", options.inputfile, "-n+1"],
                                 stdout=subprocess.PIPE)

        self.write("<pre>")
        self.write("Hello, world\n")
        self.flush()

        self.stream = tornado.iostream.PipeIOStream(self.p.stdout.fileno())
        self.stream.read_until("\n", self.line_from_nettail)

    def on_connection_close(self, *args, **kwargs):
        """Clean up the nettail process when the connection is closed.
        """

        print "CONNECTION CLOSED !!!"
        self.p.terminate()
        super(MainHandler, self).on_connection_close(*args, **kwargs)

    def line_from_nettail(self, data):
        self.write(data)
        self.flush()
        self.stream.read_until("\n", self.line_from_nettail)


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test")


class ShellHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        from async_process import call_subprocess
        self.write("Before sleep<br />")
        self.flush()
        response = yield tornado.gen.Task(call_subprocess, self, "sleep 5")
        response = yield tornado.gen.Task(call_subprocess, self, "ls /")
        self.write("Output is:\n%s" % (response.read(),))
        self.finish()


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/b", ShellHandler),
        (r"/a", MainHandler),
        (r"/test", TestHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


