# modelhub_core/db_manager.py
import os
import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        # Opcionalmente, podrías crear la tabla si no existe.

    def init_db(self):
        """Crea la tabla 'models' si no existe."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                source TEXT,  -- 'git' o 'local'
                url TEXT,     -- o 'local_path' / 'git_url'
                path TEXT NOT NULL, 
                created_at TEXT
            );
        """)
        conn.commit()
        conn.close()

    def insert_model(self, name, source, url, path):
        """Inserta un modelo en la BD."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        now = datetime.now().isoformat()
        c.execute("""
            INSERT INTO models (name, source, url, path, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (name, source, url, path, now))
        conn.commit()
        conn.close()

    def delete_model(self, name):
        """Elimina un modelo de la BD por nombre."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM models WHERE name=?", (name,))
        conn.commit()
        conn.close()

    def model_exists(self, name=None, url=None):
        """Comprueba si existe un modelo, por nombre o url."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT COUNT(*) FROM models WHERE name=? OR url=?"
        c.execute(query, (name, url))
        (count,) = c.fetchone()
        conn.close()
        return count > 0

    def list_models(self):
        """Devuelve una lista con todos los modelos."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT name, source, url, path, created_at FROM models")
        rows = c.fetchall()
        conn.close()
        return rows