#!/usr/bin/env python3
"""HTTP server for Coolify: dynamic landing page + /health."""
import html
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "3000"))
TEMPLATE = "/app/web/index.html"


def _ctx():
    hostname = socket.gethostname()
    coolify_container = os.environ.get("COOLIFY_CONTAINER_NAME", "").strip()
    fqdn = os.environ.get("COOLIFY_FQDN", "").strip()
    coolify_url = os.environ.get("COOLIFY_URL", "").strip()

    if coolify_container:
        raw_exec = (
            f"docker exec -it {coolify_container} /usr/bin/imapsync \\\n"
            f"  --host1 imap.source.example --user1 you --password1 secret \\\n"
            f"  --host2 imap.dest.example --user2 you --password2 secret"
        )
        container_hint = (
            "<p>Coolify exposes <code>COOLIFY_CONTAINER_NAME</code> as "
            f"<strong>{html.escape(coolify_container)}</strong>. Use that name after "
            "<code>docker exec -it</code> on the Docker host.</p>"
        )
    else:
        raw_exec = (
            "docker exec -it <container> /usr/bin/imapsync \\\n"
            "  --host1 imap.source.example --user1 you --password1 secret \\\n"
            "  --host2 imap.dest.example --user2 you --password2 secret"
        )
        container_hint = (
            "<p>Could not read <code>COOLIFY_CONTAINER_NAME</code>. On the server, run "
            "<code>docker ps</code> and use your app’s container name instead of "
            "<code>&lt;container&gt;</code>. "
            f"Inside this container, hostname is <code>{html.escape(hostname)}</code> "
            "(often different from the Docker name).</p>"
        )

    public_url = ""
    if coolify_url:
        public_url = (
            f'<p>Public URL (this page): <a href="{html.escape(coolify_url)}">'
            f"{html.escape(coolify_url)}</a></p>"
        )
    elif fqdn:
        public_url = f'<p>Host: <code>{html.escape(fqdn)}</code></p>'

    return {
        "HOSTNAME": html.escape(hostname),
        "CONTAINER_HINT": container_hint,
        "DOCKER_EXEC": html.escape(raw_exec),
        "PUBLIC_URL": public_url,
    }


def render_page():
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    c = _ctx()
    for key, val in c.items():
        tpl = tpl.replace("{{" + key + "}}", val)
    return tpl


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"OK\n")
            return
        if path in ("/", "/index.html"):
            body = render_page().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404, "Not Found")


def main():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
