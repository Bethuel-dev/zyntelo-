import http.server, os, sys
# Racine du dépôt (dossier parent de tests/) : index.html, vendor/, sw.js…
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a): pass
    def do_GET(self):
        path = self.path.split('?')[0]
        if path.startswith('/vendor/') or '.' in os.path.basename(path):
            return super().do_GET()          # fichier statique (404 s'il manque)
        self.path = '/index.html'            # comme Vercel : routes SPA -> index.html
        return super().do_GET()
http.server.ThreadingHTTPServer(('127.0.0.1', 8765), H).serve_forever()
