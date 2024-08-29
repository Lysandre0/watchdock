from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from ..utils.db_utils import get_redirections_from_db

class ReverseProxy:
    def __init__(self, app):
        """Initialise le reverse proxy avec une application Flask."""
        self.app = app
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    def load_proxy_rules(self):
        """Charge les règles de redirection à partir de la base de données."""
        redirections = get_redirections_from_db()
        for domain, url in redirections.items():
            # Pour chaque redirection, crée une route dans Flask
            self.app.add_url_rule(
                f"/{domain}.local/", 
                endpoint=domain,
                view_func=lambda: (f"Redirection vers {url}", 302),
                methods=["GET"]
            )

    def start(self):
        """Démarre l'application Flask."""
        self.app.run(host='0.0.0.0', port=5000)

def start_proxy():
    """Initialise et démarre le proxy."""
    app = Flask(__name__)
    proxy = ReverseProxy(app)
    proxy.load_proxy_rules()
    proxy.start()
