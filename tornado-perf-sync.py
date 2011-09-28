from tornado import ioloop, web
import sys
import pymongo

class Handler(web.RequestHandler):
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = pymongo.Connection().perftest
        return self._db

    def get(self, id):
        try:
            msg = find_one({"_id": id})
            self.write("200 OK")
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
