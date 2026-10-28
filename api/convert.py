from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os, tempfile

class handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        to = parse_qs(urlparse(self.path).query).get('to', ['docx'])[0]
        data = self.rfile.read(int(self.headers.get('content-length', 0)))
        try:
            with tempfile.TemporaryDirectory() as d:
                src = os.path.join(d, 'in.pdf')
                open(src, 'wb').write(data)
                if to == 'docx':
                    from pdf2docx import Converter
                    out = os.path.join(d, 'out.docx')
                    c = Converter(src)
                    c.convert(out)
                    c.close()
                else:
                    import fitz, openpyxl
                    wb = openpyxl.Workbook()
                    wb.remove(wb.active)
                    for i, p in enumerate(fitz.open(src)):
                        ws = wb.create_sheet('Page %d' % (i + 1))
                        found = False
                        for t in p.find_tables().tables:
                            found = True
                            for row in t.extract():
                                ws.append([c or '' for c in row])
                            ws.append([])
                        if not found:
                            for line in p.get_text().splitlines():
                                ws.append([line])
                    out = os.path.join(d, 'out.xlsx')
                    wb.save(out)
                body = open(out, 'rb').read()
            self._send(200, body, 'application/octet-stream')
        except Exception as e:
            self._send(500, str(e).encode(), 'text/plain')
