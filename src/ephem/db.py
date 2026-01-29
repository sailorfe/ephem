import sqlite3
import os
from pathlib import Path


def get_db_path():
    env_path = os.environ.get("EPHEM_DB")
    if env_path:
        return Path(env_path)

    xdg_data = os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
    return Path(xdg_data) / "ephem" / "ephem.db"


def get_connection():
    db_path = get_db_path()
    os.makedirs(db_path.parent, exist_ok=True)
    return sqlite3.connect(db_path)


def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS charts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp_utc TEXT NOT NULL,
                timestamp_input TEXT NOT NULL,
                latitude REAL,
                longitude REAL
            )
        """)
        conn.commit()


def add_chart(
    name: str, timestamp_utc: str, timestamp_input: str, latitude=None, longitude=None
):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO charts (name, timestamp_utc, timestamp_input, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """,
            (name, timestamp_utc, timestamp_input, latitude, longitude),
        )
        conn.commit()
        return cursor.lastrowid


def get_chart(chart_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, name, timestamp_utc, timestamp_input, latitude, longitude 
            FROM charts WHERE id = ?
        """,
            (chart_id,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "timestamp_utc": row[2],
                "timestamp_input": row[3],
                "latitude": row[4],
                "longitude": row[5],
            }
    return None


def view_charts():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT id, name, timestamp_utc, timestamp_input, latitude, longitude 
            FROM charts ORDER BY id
        """)
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "timestamp_utc": row[2],
                "timestamp_input": row[3],
                "latitude": row[4],
                "longitude": row[5],
            }
            for row in rows
        ]


def delete_chart(chart_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM charts WHERE id = ?", (chart_id,))
        conn.commit()
        return cursor.rowcount > 0
