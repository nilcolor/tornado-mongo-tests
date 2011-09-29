from tornado import ioloop, web
import asyncmongo

class Handler(web.RequestHandler):
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(
                pool_id        = 'perfpool',
                host           = '127.0.0.1',
                port           = 27017,
                maxcached      = 10,
                maxconnections = 500,
                dbname         = 'perftest'
            )
        return self._db

    @web.asynchronous
    def get(self, id):
        self.db.messages.find({"_id": int(id)}, limit=1, callback=self._on_response)

    def _on_response(self, response, error):
        if error:
            self.write("404 NOT FOUND")
        else:
            self.write("200 OK")
        self.finish()


app = web.Application([
    (r"/(.*)", Handler),
])

if __name__ == "__main__":
    app.listen(8888)
    ioloop.IOLoop.instance().start()
