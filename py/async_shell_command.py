#!/usr/bin/env python
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.pipe = p = os.popen('sleep 5; cat /etc/mime.types')
        self.ioloop.add_handler( p.fileno(), self.async_callback(self.on_response), self.ioloop.READ )

    def on_response(self,fd,events):
        for line in self.pipe:
            self.write( line )

        self.ioloop.remove_handler(fd)
        self.finish()

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('this is a test')

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test/", TestHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
