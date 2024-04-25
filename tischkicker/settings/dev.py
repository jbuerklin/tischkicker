import sys

from .base import BASE_DIR, CSP_IMG_SRC, STATICFILES_DIRS, VITE_DEV_MODE

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS += (
    BASE_DIR
    / "public",  # `npm run build` will copy this folder in production mode. For development mode, we need django to serve the files.
    BASE_DIR / "node_modules",
)

host, port = None, None
for i, arg in enumerate(sys.argv):
    if arg == "runserver" and len(sys.argv) > i + 1:
        *host, port = sys.argv[i + 1].split(":")

DOMAIN = f"http://{host[0] if host else 'localhost'}:{port or 8000}"

CSP_UPGRADE_INSECURE_REQUESTS = False

# Additional CSP needed for vite dev server
if VITE_DEV_MODE:
    CSP_SCRIPT_SRC_ELEM = ["'self'", f"http:"]
    CSP_CONNECT_SRC = ["'self'", f"ws:"]
    CSP_STYLE_SRC = ["'self'", "'unsafe-inline'"]
    CSP_IMG_SRC.append(f"http:")
