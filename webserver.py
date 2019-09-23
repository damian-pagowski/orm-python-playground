from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from db_server import create_session
from database_setup import Restaurant

session = create_session()

class WebServerhandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
            elif self.path.endswith("/test"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<h1>Hello from TEST!</h1>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)




def main():
    try:
        server = HTTPServer(('', 8080), WebServerhandler)
        print "Web Server Running on port 8080"
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Ctrl + C receiver. shutting down server'
        server.socket.server_close()

if __name__ == "__main__":
    main()