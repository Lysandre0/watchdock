import docker
from .models import get_db_connection
import re  # Importer la bibliothèque regex pour extraire IP et port

def get_running_containers():
    try: 
        # Connecte explicitement le client Docker
        client = docker.from_env()

        # Récupère tous les conteneurs en cours d'exécution
        containers = client.containers.list()

        # Prépare la connexion à la base de données
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Récupère tous les IDs des conteneurs en cours d'exécution
            running_container_ids = [container.id for container in containers]

            # Supprime de la base de données les conteneurs qui ne sont plus en cours d'exécution
            if running_container_ids:
                placeholders = ','.join(['?'] * len(running_container_ids))
                cursor.execute(f'DELETE FROM containers WHERE id NOT IN ({placeholders})', running_container_ids)
            else:
                # Si aucun conteneur ne tourne, vide la table
                cursor.execute('DELETE FROM containers')

            # Prépare les données des conteneurs pour l'insertion ou la mise à jour
            container_data = []
            for container in containers:
                container_name = container.name
                container_id = container.id
                container_image = container.image.tags[0] if container.image.tags else 'Unknown'

                # Récupère les labels Docker
                labels = container.attrs.get('Config', {}).get('Labels', {})
                web_ui_url = labels.get("net.unraid.docker.webui", None)

                if web_ui_url:
                    # Utilise une expression régulière pour extraire l'adresse IP et le port sans le schéma
                    match = re.search(r'//([\d\.]+):(\d+)', web_ui_url)  # Change l'expression pour ignorer le schéma
                    if match:
                        ip_address = match.group(1)  # Extrait l'adresse IP
                        port = match.group(2)       # Extrait le port

                # Crée un nom de domaine en ajoutant .local au nom du conteneur
                domain_name = f"{container_name}.local"

                # Prépare les données pour l'insertion dans la base de données
                container_data.append((container_id, container_name, container_image, ip_address, port, domain_name))

            # Insère ou met à jour les informations des conteneurs en cours d'exécution
            cursor.executemany('''
                INSERT OR REPLACE INTO containers (id, name, image, ip_address, port, domain_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', container_data)

            # Valide les transactions
            conn.commit()

    except docker.errors.DockerException as e:
        print(f"Erreur lors de l'interaction avec Docker : {e}")
        return []
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return []

    # Retourne la liste des conteneurs en cours d'exécution sous forme de dictionnaires
    return [
        {
            "name": container.name,
            "id": container.id,
            "image": container.image.tags[0] if container.image.tags else 'Unknown',
            "ip_address": ip_address,
            "port": port,
            "domain_name": f"{container.name}.local"
        }
        for container in containers
    ]
