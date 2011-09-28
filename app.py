from tornado import ioloop
from tornado import web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")

app = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

