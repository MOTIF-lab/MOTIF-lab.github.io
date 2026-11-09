#!/usr/bin/env python3
"""serve_public.py PORT DIR — static server for a Hugo `public/` build with the MIME types the showcase pages need."""
import http.server, mimetypes, os, sys
mimetypes.add_type("font/woff2", ".woff2"); mimetypes.add_type("video/mp4", ".mp4"); mimetypes.add_type("application/json", ".json"); mimetypes.add_type("image/svg+xml", ".svg")
port, root = int(sys.argv[1]), sys.argv[2]
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=root, **k)
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
