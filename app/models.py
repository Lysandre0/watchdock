import sqlite3

DATABASE = 'containers.db'

def get_db_connection():
    """Établit une connexion à la base de données SQLite et configure le retour de lignes comme des objets de type Row."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permet l'accès aux colonnes par nom
    return conn

def execute_query(query, params=()):
    """Exécute une requête SQL avec paramètres, gère les erreurs et assure la fermeture de la connexion."""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()  # Retourne les résultats de la requête
    except sqlite3.Error as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        return []
    finally:
        conn.close()  # Assure la fermeture de la connexion

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de requête pour tester la fonction
    results = execute_query('SELECT * FROM containers')
    for row in results:
        print(dict(row))  # Affiche les résultats sous forme de dictionnaires
