from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

import sys
import os


#!!! The following is necessary to make sure we can import from files in the local directory !!!
try:
    import responders
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    import responders
    sys.path.remove(os.path.dirname(__file__))


import simplejson


def Environ2RequestQuery(environ):
    d=parse_qs(environ['QUERY_STRING'])
    map={}
    for key in d:
        map[key]=d[key][0]
    return map



def application(environ, start_response):

    output=""
#    try:
    returndata=Environ2RequestQuery(environ)
    mydatatype=returndata['datatype']
    resplist=responders.GetRespList()
    if not(mydatatype in resplist):
        raise Exception("Unknown request {0}".format(mydatatype))
    else:
        returndata=resplist[mydatatype](returndata)
#    returndata['something']='some extra data'

#    except Exception, err:
#        returndata['Error']=str(err)

    output=simplejson.dumps(returndata)
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'),
                    ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
