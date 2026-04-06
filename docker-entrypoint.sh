#!/bin/sh
# Coolify sets PORT; dynamic page shows real container name for docker exec.
set -e
exec python3 /app/web/serve.py
