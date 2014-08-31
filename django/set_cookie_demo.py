# encoding: utf-8

import Cookie
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


class MyRequestHandler(SimpleHTTPRequestHandler):

    """Docstring for MyRequestHandler. """

    def do_GET(self):
        content = "<html><body>Path is: %s</body></html>" % self.path
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content)))

        cookie = Cookie.SimpleCookie()
        cookie['id'] = 'some_value_42'
        cookie['web'] = 'web'
        self.wfile.write(cookie.output())
        self.wfile.write('\r\n')

        self.end_headers()
        self.wfile.write(content)


server = HTTPServer(('', 8900), MyRequestHandler)
server.serve_forever()
