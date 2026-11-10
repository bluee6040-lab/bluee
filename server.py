#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8080

class DownloadHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Force download for PDF and ZIP files
        if self.path.endswith('.pdf'):
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', 'attachment; filename="PD_Detector_Complete_Manual.pdf"')
        elif self.path.endswith('.zip'):
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="PD_Detector_Complete_Package.zip"')
        super().end_headers()

if __name__ == '__main__':
    os.chdir('/home/user/bluee')
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('0.0.0.0', PORT), DownloadHandler) as httpd:
        print(f"Serving download portal on port {PORT}")
        httpd.serve_forever()
