import docker
from .db_utils import get_db_connection
import re

def get_running_containers():
    """Récupère les conteneurs Docker en cours d'exécution et met à jour la base de données."""
    try:
        client = docker.from_env()
        containers = client.containers.list()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            running_container_ids = [container.id for container in containers]

            # Mise à jour de la base de données : suppression des conteneurs non actifs
            placeholders = ','.join(['?'] * len(running_container_ids))
            cursor.execute(f'DELETE FROM containers WHERE id NOT IN ({placeholders})', running_container_ids) if running_container_ids else cursor.execute('DELETE FROM containers')

            for container in containers:
                container_name = container.name
                container_id = container.id
                container_image = container.image.tags[0] if container.image.tags else 'Unknown'

                # Récupération des labels pour l'URL de l'UI Web, si présente
                labels = container.attrs.get('Config', {}).get('Labels', {})
                web_ui_url = labels.get("net.unraid.docker.webui")

                # Extraction de l'IP et du port depuis l'URL de l'UI Web si disponible
                match = re.search(r'//([\d\.]+):(\d+)', web_ui_url) if web_ui_url else None
                ip_address, port = match.groups() if match else ('localhost', '80')

                # Récupération des informations réseau si l'URL de l'UI Web n'est pas disponible
                if not match:
                    networks = container.attrs.get('NetworkSettings', {}).get('Networks', {})
                    ip_address = next(iter(networks.values()), {}).get('IPAddress', 'localhost')
                    ports = container.attrs.get('NetworkSettings', {}).get('Ports', {})
                    port = next((p[0]['HostPort'] for p in ports.values() if p), '80')

                # Mettre à jour la base de données avec les informations du conteneur
                cursor.execute('''
                    INSERT OR REPLACE INTO containers (id, name, image, ip_address, port)
                    VALUES (?, ?, ?, ?, ?)
                ''', (container_id, container_name, container_image, ip_address, port))

            conn.commit()

    except docker.errors.DockerException as e:
        print(f"Erreur lors de l'interaction avec Docker : {e}")
        return []
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return []

    # Retourne les conteneurs avec les informations récupérées
    return [
        {
            "name": container.name,
            "id": container.id,
            "image": container.image.tags[0] if container.image.tags else 'Unknown',
            "ip_address": next((network.get('IPAddress', 'localhost') for network in container.attrs.get('NetworkSettings', {}).get('Networks', {}).values()), 'localhost'),
            "port": next((port[0]['HostPort'] for port in container.attrs.get('NetworkSettings', {}).get('Ports', {}).values() if port), '80')
        }
        for container in containers
    ]
