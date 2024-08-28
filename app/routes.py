from flask import Blueprint, jsonify, render_template
from .docker_utils import get_running_containers

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    """Affiche la page d'accueil."""
    return render_template('index.html')

@main.route('/containers', methods=['GET'])
def list_containers():
    """Retourne la liste des conteneurs en cours d'exécution sous forme de JSON."""
    try:
        containers = get_running_containers()
        return jsonify(containers)
    except Exception as e:
        # Gestion des erreurs pour le cas où `get_running_containers` échoue
        return jsonify({"error": "Une erreur est survenue lors de la récupération des conteneurs."}), 500
