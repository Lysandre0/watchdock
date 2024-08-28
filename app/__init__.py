from flask import Flask
from .database import init_db  # Assure-toi que l'importation relative est correcte

def create_app():
    app = Flask(__name__)

    # Initialisation de la base de données
    init_db()  # N'appelle pas avec des arguments si la fonction ne prend pas d'arguments

    # Importation des routes
    from .routes import main
    app.register_blueprint(main)

    return app