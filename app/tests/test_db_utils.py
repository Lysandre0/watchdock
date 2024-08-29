import unittest
from ..utils.db_utils import get_db_connection, execute_query

class TestDatabaseUtils(unittest.TestCase):

    def setUp(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_connection(self):
        """Test la connexion à la base de données."""
        self.assertIsNotNone(self.conn)

    def test_execute_query(self):
        """Test l'exécution d'une requête SQL."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            value TEXT
        )
        '''
        insert_query = 'INSERT INTO test_table (value) VALUES (?)'
        select_query = 'SELECT value FROM test_table'

        self.cursor.execute(create_table_query)
        self.conn.commit()

        execute_query(insert_query, ('test_value',))
        result = execute_query(select_query)
        self.assertEqual(result[0]['value'], 'test_value')

if __name__ == '__main__':
    unittest.main()
