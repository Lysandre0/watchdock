from .models import get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Création de la table si elle n'existe pas déjà
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS containers (
        id TEXT PRIMARY KEY,
        name TEXT,
        image TEXT,
        ip_address TEXT,
        port INTEGER
    )
    ''')
    conn.commit()
    conn.close()