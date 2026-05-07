#!/usr/bin/env python3
"""
Simple HTTP server with client-side routing support.
Serves static files normally, but serves index.html for routes without file extensions.
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class RoutingHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler that supports client-side routing."""

    def do_GET(self):
        # Parse the path
        path = self.path.split('?')[0]  # Remove query string
        
        # If it's a file with an extension, serve it normally
        if '.' in path.split('/')[-1]:
            return super().do_GET()
        
        # If it's a directory request, try to serve index.html
        if path.endswith('/') or path == '':
            self.path = '/index.html'
            return super().do_GET()
        
        # For routes without extensions (like /store, /team), serve index.html
        self.path = '/index.html'
        return super().do_GET()

    def end_headers(self):
        """Add headers to prevent caching of HTML files."""
        if self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

    def log_message(self, format, *args):
        """Log requests in a cleaner format."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """Start the HTTP server."""
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, RoutingHTTPRequestHandler)
    
    print(f"🚀 Server running at http://localhost:{port}")
    print(f"📁 Serving files from: {script_dir}")
    print("Press Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
