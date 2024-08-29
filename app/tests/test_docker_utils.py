import unittest
from unittest.mock import patch, MagicMock
from ..utils.docker_utils import get_running_containers

class TestDockerUtils(unittest.TestCase):

    @patch('app.docker_utils.docker.from_env')
    def test_get_running_containers(self, mock_docker_from_env):
        """Test la récupération des conteneurs Docker."""
        mock_client = MagicMock()
        mock_container = MagicMock()
        mock_container.id = 'container_id'
        mock_container.name = 'container_name'
        mock_container.image.tags = ['image_tag']
        mock_container.attrs = {
            'Config': {
                'Labels': {
                    'net.unraid.docker.webui': 'http://192.168.1.100:5432'
                }
            }
        }
        mock_client.containers.list.return_value = [mock_container]
        mock_docker_from_env.return_value = mock_client

        containers = get_running_containers()
        self.assertEqual(len(containers), 1)
        self.assertEqual(containers[0]['name'], 'container_name')
        self.assertEqual(containers[0]['ip_address'], '192.168.1.100')
        self.assertEqual(containers[0]['port'], 5432)

if __name__ == '__main__':
    unittest.main()
