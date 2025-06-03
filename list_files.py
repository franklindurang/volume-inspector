import http.server
import socketserver
import os
import json

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            list_dir(self)
        else:
            super().do_GET()

def list_dir(handler):
    directory = handler.words[1] if len(handler.words) > 1 else "/data"
    try:
        files = os.listdir(directory)
        handler.send_response(200)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(files).encode())
    except FileNotFoundError:
        handler.send_response(404)
        handler.end_headers()
    except PermissionError:
        handler.send_response(403)
        handler.end_headers()

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            list = os.listdir('/data')
            list_html = "<ul>" + "".join(f"<li>{item}</li>" for item in list) + "</ul>"
            output = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Volume Contents</title>
            </head>
            <body>
                <h1>Contents of /data</h1>
                {list_html}
            </body>
            </html>
            """
            self.wfile.write(output.encode())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
