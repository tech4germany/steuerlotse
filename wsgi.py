from app import app

from werkzeug.middleware.proxy_fix import ProxyFix
app = ProxyFix(app, x_for=1, x_host=1)

if __name__ == "__main__":
    app.run()
