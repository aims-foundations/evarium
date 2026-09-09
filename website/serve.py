#!/usr/bin/env python3
"""Local preview server that behaves like production.

`python -m http.server` misrepresents this site badly enough to send you
chasing phantoms. It speaks HTTP/1.0 (so every asset, including every 304,
opens a fresh TCP connection), sends no `Content-Encoding`, and sends no
`Cache-Control`. Measured against the live GitHub Pages copy, that makes
`runs.json` 482 KB instead of 55 KB and a `frames.json` 446 KB instead of
120 KB, and it makes a warm reload slower than a cold one because the browser
revalidates every heuristically-cached entry over non-reusable connections.

This server fixes the three differences so what you test resembles what ships:

  HTTP/1.1 with keep-alive
  gzip for compressible types, when the client asks for it
  Cache-Control roughly matching the Render header policy

Usage:
    python website/serve.py            # serves website/client on :8000
    python website/serve.py -p 8001
    python website/serve.py -d some/other/dir

This file lives in `website/`, not `website/client/`, because `client/` is the
deploy root and has to stay purely static.
"""

import argparse
import functools
import gzip
import io
import mimetypes
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Python's mimetypes table predates these; without them woff2 goes out as
# application/octet-stream, which is not what Render or Pages send.
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/woff", ".woff")
mimetypes.add_type("image/svg+xml", ".svg")

# Types worth compressing. Fonts and images are already compressed.
COMPRESSIBLE = {".html", ".css", ".js", ".json", ".svg", ".txt", ".map", ".csv"}

# Below this, the gzip header costs more than it saves.
MIN_COMPRESS_BYTES = 1024


class Handler(SimpleHTTPRequestHandler):
    # The single most important line here: HTTP/1.0 is what kills keep-alive.
    protocol_version = "HTTP/1.1"

    def cache_control(self, url_path: str) -> str:
        # Mirrors the policy render.yaml should carry: HTML revalidates every
        # time so a deploy is visible immediately, data and assets are cached.
        if url_path.endswith(".html") or url_path.endswith("/"):
            return "no-cache"
        if "/data/" in url_path or url_path.endswith("runs.json"):
            return "public, max-age=600"
        return "public, max-age=3600"

    def send_head(self):
        path = self.translate_path(self.path)

        # Let the base class handle directory redirects and index lookup, then
        # come back through here for the resolved file.
        if os.path.isdir(path):
            if not self.path.endswith("/"):
                return super().send_head()
            for index in ("index.html", "index.htm"):
                candidate = os.path.join(path, index)
                if os.path.isfile(candidate):
                    path = candidate
                    break
            else:
                return super().send_head()

        if not os.path.isfile(path):
            return super().send_head()

        try:
            with open(path, "rb") as fh:
                raw = fh.read()
        except OSError:
            self.send_error(404, "File not found")
            return None

        ext = os.path.splitext(path)[1].lower()
        accepts_gzip = "gzip" in self.headers.get("Accept-Encoding", "")
        body = raw
        encoding = None
        if accepts_gzip and ext in COMPRESSIBLE and len(raw) >= MIN_COMPRESS_BYTES:
            body = gzip.compress(raw, 6)
            encoding = "gzip"

        self.send_response(200)
        self.send_header("Content-type", self.guess_type(path))
        self.send_header("Content-Length", str(len(body)))
        if encoding:
            self.send_header("Content-Encoding", encoding)
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Cache-Control", self.cache_control(self.path))
        self.end_headers()
        return io.BytesIO(body)


def main() -> None:
    default_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-p", "--port", type=int, default=8000)
    ap.add_argument("-b", "--bind", default="127.0.0.1")
    ap.add_argument("-d", "--directory", default=default_dir)
    args = ap.parse_args()

    if not os.path.isdir(args.directory):
        print(f"No such directory: {args.directory}", file=sys.stderr)
        sys.exit(1)

    handler = functools.partial(Handler, directory=args.directory)
    with ThreadingHTTPServer((args.bind, args.port), handler) as httpd:
        print(f"Serving {args.directory}")
        print(f"  http://{args.bind}:{args.port}/")
        print("  HTTP/1.1 keep-alive, gzip, Cache-Control. Ctrl-C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
