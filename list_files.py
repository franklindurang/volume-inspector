import http.server
import socketserver
import os
import json
import pwd
import shutil

PORT = 8080
MOUNT_POINT = "/data"
TARGET_USER = "node"

def attempt_chown(path, user):
    try:
        uid = pwd.getpwnam(user).pw_uid
        print(f"Attempting to chown {path} to UID: {uid}")
        os.chown(path, uid, -1)
        print(f"Successfully chowned {path} to user {user}")
    except KeyError:
        print(f"User {user} not found.")
    except OSError as e:
        print(f"Error chowning {path}: {e}")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            attempt_chown(MOUNT_POINT, TARGET_USER) # Attempt to change ownership
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
                <p>Attempted to change ownership to user '{TARGET_USER}'. Check server logs.</p>
                {list_html}
            </body>
            </html>
            """
            self.wfile.write(output.encode())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
