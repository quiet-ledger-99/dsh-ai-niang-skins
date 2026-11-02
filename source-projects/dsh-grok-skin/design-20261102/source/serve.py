"""Local animation/skin preview. Browser export saves only the selected theme's film."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse, json

ROOT = Path(__file__).resolve().parents[3]
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)
    def do_POST(self):
        theme = self.path.removeprefix('/export/')
        if self.path != '/export/' + theme or theme not in ('grok', 'deepseek'):
            self.send_error(404); return
        size = int(self.headers.get('Content-Length', '0'))
        if not 0 < size < 100_000_000:
            self.send_error(413); return
        out = ROOT / ('dsh-' + theme + '-skin/design-20261102/source/motion-v1.webm')
        out.write_bytes(self.rfile.read(size))
        self.send_response(200); self.end_headers(); self.wfile.write(b'saved')
    def log_message(self, *args):
        pass
if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8772)
    args=parser.parse_args();print('Preview at http://127.0.0.1:%s/' % args.port, flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
