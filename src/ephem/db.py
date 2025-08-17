import sqlite3
import os
from pathlib import Path

def get_db_path(cli_path=None):
    """Return the SQLite DB path, checking CLI arg, env var, or default config location."""
    if cli_path:
        return cli_path
    env_path = os.environ.get("EPHEM_DB")
    if env_path:
        return env_path
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return config_home / "ephem" / "ephem.db"

def get_connection(cli_path=None):
    db_path = get_db_path(cli_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # ensure folder exists
    return sqlite3.connect(db_path)

def create_tables(cli_path=None):
    with get_connection(cli_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ephemdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp_utc TEXT NOT NULL,
                timestamp_input TEXT NOT NULL,
                latitude REAL,
                longitude REAL
            )
        """)
        conn.commit()

def add_chart(name: str, timestamp_utc: str, timestamp_input: str,
              latitude=None, longitude=None, cli_path=None):
    with get_connection(cli_path) as conn:
        conn.execute("""
            INSERT INTO ephemdata (name, timestamp_utc, timestamp_input, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """, (name, timestamp_utc, timestamp_input, latitude, longitude))

def view_charts(cli_path=None):
    try:
        with get_connection(cli_path) as conn:
            cursor = conn.execute("SELECT * FROM ephemdata ORDER BY id")
            rows = cursor.fetchall()
        return [
            {"id": r[0], "name": r[1], "timestamp_utc": r[2],
             "timestamp_input": r[3], "latitude": r[4], "longitude": r[5]}
            for r in rows
        ]
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            return []  # table doesn't exist yet, treat as empty
        raise

def get_chart(chart_id: int, cli_path=None):
    with get_connection(cli_path) as conn:
        cursor = conn.execute("SELECT * FROM ephemdata WHERE id = ?", (chart_id,))
        row = cursor.fetchone()
    if row:
        return {"id": row[0], "name": row[1], "timestamp_utc": row[2],
                "timestamp_input": row[3], "latitude": row[4], "longitude": row[5]}
    return None

def delete_chart(chart_id: int):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM ephemdata WHERE id = ?", (chart_id,))
        if cursor.rowcount == 0:
            print(f"No chart found with ID {chart_id}.")
        else:
            print(f"Deleted chart ID {chart_id}.")
