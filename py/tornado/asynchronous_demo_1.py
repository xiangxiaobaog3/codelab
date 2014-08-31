#!/usr/bin/env python
# encoding: utf-8


import tornado.web
import tornado.httpclient


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        url = "http://google.com"
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(url, callback=self.on_response)

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        # json = tornado.escape.json_decode(response.body)
        self.write(response.body)
        self.finish()


def main():
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
