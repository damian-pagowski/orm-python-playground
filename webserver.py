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
                    output += '</br><a href="/restaurants/{}/edit">Edit</a>'.format( restaurant.id )
                    output += "</br><a href=\"#delete\">Delete</a>"
                    output += "</br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'restaurantName' type = 'text' placeholder = 'Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"

                self.wfile.write(output)
                return
            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'restaurantName' type = 'text' placeholder = 'Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"

                self.wfile.write(output)
                return
            elif self.path.endswith("/edit"):
                spl = self.path.split('/')
                restaurant_id = spl[-2]
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/" + restaurant_id + "/edit'>"
                output += "<input name = 'restaurantName' type = 'text' placeholder = '%s' >" % restaurant.name
                output += "<input type='submit' value='Rename'>"
                output += "</form></body></html>"

                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    def do_POST(self):
        try:
            if self.path.endswith('restaurants/new'):
                # get post params from request
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurantName')
                    # create restaurant in database
                    restaurant = Restaurant()
                    restaurant.name=messagecontent[0]
                    session.add(restaurant)
                    session.commit()
                    # send response - redirect to restaurant list
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            elif self.path.endswith('/edit'):
                # get post params from request
                spl = self.path.split('/')
                restaurant_id = int(spl[-2])

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurantName')
                    # get restaurant from database

                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first() 
                    restaurant.name=messagecontent[0]
                    session.add(restaurant)
                    session.commit()
                    # send response - redirect to restaurant list
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass



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