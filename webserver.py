from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Column, ForeignKey, Integer, String
from db_server import create_session
from entities import Restaurant
# from sqlalchemy.ext.declarative import declarative_base

# Create session and connect to DB
session = create_session()
# DB mapping
# Base = declarative_base()

# class Restaurant(Base):
#     __tablename__ = "restaurant"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)


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