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

            if running_container_ids:
                placeholders = ','.join(['?'] * len(running_container_ids))
                cursor.execute(f'DELETE FROM containers WHERE id NOT IN ({placeholders})', running_container_ids)
            else:
                cursor.execute('DELETE FROM containers')

            container_data = []
            for container in containers:
                container_name = container.name
                container_id = container.id
                container_image = container.image.tags[0] if container.image.tags else 'Unknown'

                labels = container.attrs.get('Config', {}).get('Labels', {})
                web_ui_url = labels.get("net.unraid.docker.webui", None)

                if web_ui_url:
                    match = re.search(r'//([\d\.]+):(\d+)', web_ui_url)
                    if match:
                        ip_address = match.group(1)
                        port = match.group(2)
                else:
                    ip_address = "0"
                    port = 0

                container_data.append((container_id, container_name, container_image, ip_address, port))

            cursor.executemany('''
                INSERT OR REPLACE INTO containers (id, name, image, ip_address, port)
                VALUES (?, ?, ?, ?, ?)
            ''', container_data)

            conn.commit()

    except docker.errors.DockerException as e:
        print(f"Erreur lors de l'interaction avec Docker : {e}")
        return []
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return []

    return [
        {
            "name": container.name,
            "id": container.id,
            "image": container.image.tags[0] if container.image.tags else 'Unknown',
            "ip_address": ip_address,
            "port": port,
        }
        for container in containers
    ]
