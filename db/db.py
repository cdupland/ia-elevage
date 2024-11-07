import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "database.db"  # Chemin de la base de données


# Gestionnaire de contexte pour gérer les connexions
@contextmanager
def connect_db():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


# Classe responsable de la base de données
class DatabaseHandler:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        # Crée la table si elle n'existe pas encore
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS prompts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                type TEXT NOT NULL,
                                structure TEXT NOT NULL,
                                prompt TEXT NOT NULL
                              );''')

            if not self._is_data_present(cursor):
                self._load_default_data(cursor)

    def _is_data_present(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM prompts;")
        return cursor.fetchone()[0] > 0

    def _load_default_data(self, cursor):
        data = [
            {"type": "beef_cattle", "structure": "small", "prompt": "small"},
            {"type": "beef_cattle", "structure": "gaec", "prompt": "gaec"},
            {"type": "beef_cattle", "structure": "gaec_bis", "prompt": "gaec_bis"},
            {"type": "dairy_cattle", "structure": "small", "prompt": "small"},
            {"type": "dairy_cattle", "structure": "medium", "prompt": "medium"},
            {"type": "dairy_cattle", "structure": "out", "prompt": "out"},
        ]
        
        for record in data:
            cursor.execute(
                "INSERT INTO prompts (type, structure, prompt) VALUES (:type, :structure, :prompt);",
                record
            )
        cursor.connection.commit()

    def get_prompts(self):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prompts;")
            return cursor.fetchall()

    def get_prompt_by_filters(self, type_=None, structure=None):
        with connect_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM prompts"
            conditions = []
            params = []

            if type_:
                conditions.append("type = ?")
                params.append(type_)
            if structure:
                conditions.append("structure = ?")
                params.append(structure)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)


            cursor.execute(query, params)

            # Fetch and return the result
            result = cursor.fetchone()
                        
            return result
    
    def add_prompt(self, type_, structure, prompt):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO prompts (type, structure, prompt) VALUES (?, ?, ?);", (type_, structure, prompt))

    def update_prompt(self, prompt_id, type_=None, structure=None, prompt=None):
        with connect_db() as conn:
            cursor = conn.cursor()
            query = "UPDATE prompts SET "
            fields = []
            params = []
            if type_:
                fields.append("type = ?")
                params.append(type_)
            if structure:
                fields.append("structure = ?")
                params.append(structure)
            if prompt:
                fields.append("prompt = ?")
                params.append(prompt)
            query += ", ".join(fields) + " WHERE id = ?;"
            params.append(prompt_id)
            cursor.execute(query, params)
