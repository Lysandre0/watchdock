import os

# Définit le répertoire de base du projet
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Définit le chemin vers le fichier de la base de données
DATABASE_PATH = os.path.join(BASE_DIR, 'app', 'containers.db')