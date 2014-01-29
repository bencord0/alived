#!/usr/bin/env python

import re
from wsgiref.simple_server import make_server
from wsgiref.util import application_uri, request_uri


class wsgiapp(object):
    def get_route(self, environ):
        route = request_uri(environ).split(
            application_uri(environ), 1)[1].split('?')
        return (route.pop(0), '?'.join(route))

    def __call__(self, environ, start_response):
        try:
            # Quick Static routes
            wsgi_request = {
                'ping': ping_route,
            }[self.get_route(environ)[0]]
        except KeyError:
            # Fallback Regex routes
            route_map = {
                '(.*)': notfound_route,
            }
            for route, func in route_map.items():
                if re.match(route, self.get_route(environ)[0]):
                    wsgi_request = func
                    break

        wsgiter = wsgi_request(environ, start_response)
        for chunk in wsgiter:
            if not isinstance(chunk, bytes):
                yield chunk.encode('utf-8')
            else:
                yield chunk
        if 'close' in wsgiter:
            wsgiter.close()


def ping_route(environ, start_response):
    start_response("200 OK", [
        ('content-type', 'application/json'),
    ])
    return ["Hello World\n"]


def notfound_route(environ, start_response):
    start_response("404 Not Found", [
        ('content-type', 'text/plain'),
    ])
    return ["Not Found\n"]

app = wsgiapp()
if __name__ == '__main__':
    import os
    httpd = make_server(
        os.environ.get('IP', ''),
        int(os.environ.get('PORT', 8000)),
        app)
    httpd.serve_forever()
