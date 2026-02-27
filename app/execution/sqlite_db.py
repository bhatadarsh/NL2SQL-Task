import sqlite3

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute_query(sql_query):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(sql_query)

        rows = cursor.fetchall()

        if cursor.description:
            columns = [d[0] for d in cursor.description]
        else:
            columns = []

        conn.close()

        return columns, rows

    except Exception as e:

        conn.close()

        return None, str(e)
