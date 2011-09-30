# encoding: utf-8
from twisted.internet import reactor
from twisted.web import server, resource
from twisted.web.server import NOT_DONE_YET
import txmongo

# import sys
# from twisted.python import log
# log.startLogging(sys.stdout)

db = txmongo.lazyMongoConnectionPool().perftest.messages


class Root(resource.Resource):
    isLeaf = True

    def _success(self, value, request):
        counter = 0
        for m in value:
            counter += len(m['longStringAttribute'])
        request.write('200 OK. Char counter = %i' % counter)
        request.finish()

    def _failure(self, error, request):
        request.setResponseCode(404)
        request.write("Invalid request")
        request.finish()

    def render_GET(self, request):
        id = int(request.uri.rsplit('/', 1)[-1])
        d = db.find({"_id": id}, limit=50)
        d.addCallback(self._success, request)
        d.addErrback(self._failure, request)
        return NOT_DONE_YET


site = server.Site(Root())
reactor.listenTCP(8888, site)

print '*' * 80
print '  Server started'
print '*' * 80

reactor.run()
