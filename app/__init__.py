from flask import Flask
from .utils.db_utils import init_db

# Importation correcte du blueprint
from .routes.main import main

def create_app():
    app = Flask(__name__)
    init_db()
    
    # Enregistrement du blueprint correctement
    app.register_blueprint(main)

    return app

def run_flask():
    app = create_app()
    app.run(host="0.0.0.0", port=5000)