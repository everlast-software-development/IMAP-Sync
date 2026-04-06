#!/bin/sh
# Coolify (and similar) set PORT; keep a process alive and serve a static page.
set -e
PORT="${PORT:-3000}"
exec python3 -m http.server "$PORT" --bind 0.0.0.0 --directory /app/web
