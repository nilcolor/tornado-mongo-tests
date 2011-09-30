from tornado import ioloop, web#, httpserver
# import sys
import pymongo

class Handler(web.RequestHandler):
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = pymongo.Connection().perftest
        return self._db

    def get(self, id):
        try:
            msg = self.db.messages.find().limit(50)
            counter = 0
            for m in msg:
                counter += len(m['longStringAttribute'])
            self.write("200 OK. Char counter = %i" % counter)
        except:
            self.write("404 NOT FOUND")

app = web.Application([
    (r"/(.*)", Handler),
])

if __name__ == "__main__":
    app.listen(8888)
    print "*" * 80
    print " Server started"
    print "*" * 80
    ioloop.IOLoop.instance().start()

# db = pymongo.Connection().perftest

# def rhandler(request):
#     try:
#         # db = pymongo.Connection().perftest
#         id = int(request.uri.rsplit('/', 1)[-1])
#         msg = db.messages.find_one({"_id": id})
#         message = "200 OK"
#         request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
#     except:
#         request.write("404 NOT FOUND")

#     request.finish()


# http_server = httpserver.HTTPServer(rhandler)
# http_server.bind(8888)
# http_server.start(0) # Forks multiple sub-processes
# ioloop.IOLoop.instance().start()
