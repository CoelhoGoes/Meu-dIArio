import psycopg
from psycopg.rows import dict_row
from connections.postgres import PostgresConnection


# -----------------------------
# FOLDERS
# -----------------------------
def create_folder(user_id: int, name: str, parent_id: int = None):
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor(row_factory=dict_row) as cur:   
            # Se for subpasta → validar se o pai pertence ao mesmo usuário
            if parent_id is not None:
                cur.execute("""
                    SELECT id FROM folders
                    WHERE id = %s AND user_id = %s
                """, (parent_id, user_id))
                parent = cur.fetchone()
                if not parent:
                    return None  # Pai não existe ou não pertence ao user

            cur.execute("""
                INSERT INTO folders (user_id, parent_id, name)
                VALUES (%s, %s, %s)
                RETURNING id, name, parent_id
            """, (user_id, parent_id, name))
            folder = cur.fetchone()
            conn.commit()
            return folder
    finally:
        conn.close()


def list_folders(user_id: int):
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT id, name, parent_id, created_at, updated_at
                FROM folders
                WHERE user_id = %s
                ORDER BY created_at
            """, (user_id,))
            return cur.fetchall()
    finally:
        conn.close()


def delete_folder(user_id: int, folder_id: int) -> bool:
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM folders
                WHERE id = %s AND user_id = %s
            """, (folder_id, user_id))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted
    finally:
        conn.close()


# -----------------------------
# NOTES
# -----------------------------
def create_note(user_id: int, folder_id: int, title: str, content: str):
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            # validar se a pasta pertence ao usuário
            cur.execute("""
                SELECT id FROM folders
                WHERE id = %s AND user_id = %s
            """, (folder_id, user_id))
            folder = cur.fetchone()
            if not folder:
                return None  # Pasta não existe ou não pertence ao user

            cur.execute("""
                INSERT INTO notes (folder_id, title, content)
                VALUES (%s, %s, %s)
                RETURNING id, title, content, folder_id
            """, (folder_id, title, content))
            note = cur.fetchone()
            conn.commit()
            return note
    finally:
        conn.close()


def list_notes(user_id: int, folder_id: int):
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT n.id, n.title, n.content, n.folder_id, n.created_at, n.updated_at
                FROM notes n
                JOIN folders f ON f.id = n.folder_id
                WHERE f.id = %s AND f.user_id = %s
                ORDER BY n.created_at
            """, (folder_id, user_id))
            return cur.fetchall()
    finally:
        conn.close()


def delete_note(user_id: int, note_id: int) -> bool:
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM notes
                WHERE id = %s
                AND folder_id IN (
                    SELECT id FROM folders WHERE user_id = %s
                )
            """, (note_id, user_id))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted
    finally:
        conn.close()
