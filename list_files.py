import http.server
import socketserver
import os
import json
import stat
import sys
import time

PORT = 8080
MOUNT_POINT = "/data"

def attempt_chmod(path, mode):
    try:
        print(f"Attempting chmod {path} to {oct(mode)}...", file=sys.stdout, flush=True)
        os.chmod(path, mode)
        print(f"Successfully chmodded {path} to {oct(mode)}", file=sys.stdout, flush=True)
    except OSError as e:
        print(f"Error chmodding {path}: {e}", file=sys.stderr, flush=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            attempt_chmod(MOUNT_POINT, 0o777)
            time.sleep(1) # Add a small delay
            list = os.listdir(MOUNT_POINT)
            list_html = "<ul>" + "".join(f"<li>{item}</li>" for item in list) + "</ul>"
            output = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Volume Contents</title>
            </head>
            <body>
                <h1>Contents of {MOUNT_POINT}</h1>
                <p>Attempted to chmod '{MOUNT_POINT}' to 0777. Check server logs.</p>
                {list_html}
            </body>
            </html>
            """
            self.wfile.write(output.encode())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}", file=sys.stdout, flush=True)
    httpd.serve_forever()
