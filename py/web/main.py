# encoding: utf-8

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World")

class ChatHandler(tornado.web.RequestHandler):
    def post(self):
        print(self.request.arguments)
        self.write('0')


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/chat", ChatHandler),
], settings={'debug':True})

if __name__ == '__main__':
    application.listen(8002)
    tornado.ioloop.IOLoop.instance().start()
