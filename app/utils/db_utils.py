import sqlite3

DATABASE = 'containers.db'

def get_db_connection():
    """Établit une connexion à la base de données SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialise la base de données SQLite en créant les tables nécessaires."""
    conn = get_db_connection()
    cursor = conn.cursor()

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

def get_redirections_from_db():
    """Charge les redirections depuis la table `containers` de la base de données SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name, ip_address, port FROM containers')
    rows = cursor.fetchall()
    conn.close()

    redirections = {}
    for row in rows:
        domain, ip, port = row
        redirections[domain] = f"{ip}:{port}"

    return redirections
