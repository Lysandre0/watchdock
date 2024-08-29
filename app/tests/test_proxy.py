import unittest
import requests

class ProxyTestCase(unittest.TestCase):

    def setUp(self):
        # Point de départ du proxy (mettre à jour avec l'URL correcte)
        self.base_url = "http://localhost:5000"  

    def test_redirection_postgres(self):
        """Test de la redirection du domaine local postgres.local"""
        try:
            response = requests.get("http://postgres.local")
            self.assertEqual(response.status_code, 200)
            self.assertIn("PostgreSQL", response.text)
        except requests.exceptions.RequestException as e:
            self.fail(f"Erreur de connexion : {e}")

    def test_redirection_another_container(self):
        """Test de la redirection pour un autre conteneur (exemple : nginx)"""
        try:
            response = requests.get("http://nginx.local")
            self.assertEqual(response.status_code, 200)
            self.assertIn("Nginx", response.text)
        except requests.exceptions.RequestException as e:
            self.fail(f"Erreur de connexion : {e}")

if __name__ == '__main__':
    unittest.main()
