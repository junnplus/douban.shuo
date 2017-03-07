from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from workflow import Workflow3
wf = Workflow3()


class TokenRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        query = dict(q.split("=") for q in query.split("&"))
        wf.cached_data('access_token', lambda: query['access_token'])
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()
        self.wfile.write('access_token: ' + query['access_token'])
        self.wfile.close()
        return


if __name__ == '__main__':
    httpd = HTTPServer(('', 4040), TokenRequestHandler)
    httpd.serve_forever()
