
from http.server import BaseHTTPRequestHandler, HTTPServer


class CustomHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Handling of GET requests
        :return:
        """
        if self.path == "/example":
                
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
                
            self.wfile.write(bytes("<html><head><title>Distributed Systems</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>Example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
    
            

if __name__ == "__main__":
    ws = HTTPServer(("127.0.0.1", 5620), CustomHttpServer)
    print(f"Started server on port 5620")

    try:
        
        ws.serve_forever()
    except KeyboardInterrupt:
        pass

    ws.server_close()
    
    
