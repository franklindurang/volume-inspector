import http.server
import socketserver
import os
import json
import stat
import sys
import urllib.parse

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
        path = urllib.parse.unquote(self.path)
        if path.startswith('/'):
            target_path = MOUNT_POINT + path
            try:
                items = os.listdir(target_path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Contents of {target_path}</title>
                </head>
                <body>
                    <h1>Contents of {target_path}</h1>
                    <ul>
                """
                if path != '/':
                    output += f'<li><a href="../">..</a></li>'
                for item in items:
                    item_path = os.path.join(target_path, item)
                    if os.path.isdir(item_path):
                        output += f'<li><a href="{urllib.parse.quote(path + "/" + item)}">{item}/</a></li>'
                    else:
                        output += f'<li>{item}</li>'
                output += """
                    </ul>
                </body>
                </html>
                """
                self.wfile.write(output.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
            except PermissionError:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Permission denied")
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}", file=sys.stdout, flush=True)
    httpd.serve_forever()
