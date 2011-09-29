# import txmongo
# from twisted.internet import defer, reactor

# @defer.inlineCallbacks
# def example():
#     mongo = yield txmongo.MongoConnection()

#     foo = mongo.perftest  # `foo` database
#     test = foo.messages  # `test` collection

#     # fetch some documents
#     docs = yield test.find({"_id": 4657364}, limit=1)
#     for doc in docs:
#         print doc
#     # need to respond it back... how?

# if __name__ == '__main__':
#     example().addCallback(lambda ign: reactor.stop())
#     reactor.run()

from twisted.web import server, resource
from twisted.internet import reactor
from json import dumps, loads
import sys

import pymongo
DB = pymongo.Connection().perftest
find_one = DB.messages.find_one
save = DB.messages.save


class Root(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        global dumps, find_one
        try:
            id = int(request.uri.rsplit('/', 1)[-1])
            msg = find_one({"_id": id})
            # msg['id'] = msg['_id']
            # del msg['_id']
            # return dumps(msg)
            return '200 OK'
        except:
            request.setResponseCode(404)
            return "Invalid request"

site = server.Site(Root())
reactor.listenTCP(8888, site)

print '*' * 80
print '  Server started'
print '*' * 80

reactor.run()
