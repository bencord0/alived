import unittest

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from context import alived

class RequestFaker(object):
    def request(self, method, url):
        response = {}
        def start_response(code, headers):
            response['code'] = int(code.split()[0])
            response['headers'] = [
                (header[0].lower(), header[1].lower())
                for header in headers]
        url = urlparse.urlparse(url)
        environ = {
            'wsgi.url_scheme': url.scheme or 'http',
            'SERVER_NAME': url.hostname or 'localhost',
            'SERVER_PORT': str(url.port) or '80',
            'PATH_INFO': url.path,
            'QUERY_STRING': url.query,
            'REQUEST_METHOD': method,
        }
        response['body'] = self.app(environ, start_response)
        return response

class TestWsgiApp(RequestFaker, unittest.TestCase):
    def setUp(self):
        self.app = alived.app()

    def test_route(self):
	self.assertEqual(
            self.app.get_route({
                'wsgi.url_scheme': 'http',
                'SERVER_NAME': '',
                'SERVER_PORT': '',
                'PATH_INFO': '/abc',
                'QUERY_STRING': 'def&ghi=jkl',
            }),
            ("abc", "def&ghi=jkl"))

    def test_hello(self):
        response = self.request('GET', '/ping')
        self.assertEqual(
            response['code'],
            200)
        self.assertEqual(
            response['headers'],
            [('content-type', 'application/json')])
        self.assertEqual(
            ''.join(response['body']),
            "Hello World\n")

    def test_404(self):
        response = self.request('GET', '/nonexistant')
        self.assertEqual(
            response['code'],
            404)
        self.assertEqual(
            response['headers'],
            [('content-type', 'text/plain')])
        self.assertEqual(
            ''.join(response['body']),
            "Not Found\n")

if __name__ == '__main__':
	import sys
	sys.exit(unittest.main())
