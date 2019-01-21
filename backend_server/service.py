import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import json
import pyjsonrpc
from bson.json_util import dumps
import mongodb_client
import operations


SERVER_HOST = 'localhost'
SERVER_PORT = 4040


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test Method"""
    # @pyjsonrpc.rpcmethod
    # def add(self, a, b):
    #     print "add is called with %d and %d" %(a,b)
    #     return a+b

    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        print "call function in service.py"
        return operations.getNewsSummariesForUser(user_id, page_num)

    @pyjsonrpc.rpcmethod
    def logNewClickForUser(user_id, news_id):
    """logNewsClickForUser"""
    print("log_news_click_for_user is called with %s and %s" % (user_id, news_id))
    operations.logNewsClickForUser(user_id, news_id)



http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERVER_PORT),
    RequestHandlerClass=RequestHandler)

print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)
http_server.serve_forever()
