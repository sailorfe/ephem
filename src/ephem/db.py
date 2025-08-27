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
    config_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / "./local/share"))
    return config_home / "ephem" / "ephem.db"

def get_connection(cli_path=None):
    db_path = get_db_path(cli_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # ensure folder exists
    return sqlite3.connect(db_path)

def create_tables(cli_path=None):
    """Create database tables if they don't exist."""
    with get_connection(cli_path) as conn:
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

def add_chart(name: str, timestamp_utc: str, timestamp_input: str,
              latitude=None, longitude=None, cli_path=None):
    """Add a chart to the database."""
    with get_connection(cli_path) as conn:
        conn.execute("""
            INSERT INTO charts (name, timestamp_utc, timestamp_input, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """, (name, timestamp_utc, timestamp_input, latitude, longitude))
        conn.commit()

def get_chart(chart_id: int, cli_path=None):
    """Get a specific chart by ID."""
    with get_connection(cli_path) as conn:
        cursor = conn.execute("""
            SELECT id, name, timestamp_utc, timestamp_input, latitude, longitude 
            FROM charts WHERE id = ?
        """, (chart_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'timestamp_utc': row[2],
                'timestamp_input': row[3],
                'latitude': row[4],
                'longitude': row[5]
            }
    return None

def view_charts(cli_path=None):
    """View all saved charts."""
    with get_connection(cli_path) as conn:
        cursor = conn.execute("""
            SELECT id, name, timestamp_utc, timestamp_input, latitude, longitude 
            FROM charts ORDER BY id
        """)
        rows = cursor.fetchall()
        return [{
            'id': row[0],
            'name': row[1],
            'timestamp_utc': row[2],
            'timestamp_input': row[3],
            'latitude': row[4],
            'longitude': row[5]
        } for row in rows]

def delete_chart(chart_id: int, cli_path=None):
    """Delete a chart by ID."""
    with get_connection(cli_path) as conn:
        conn.execute("DELETE FROM charts WHERE id = ?", (chart_id,))
        conn.commit()
