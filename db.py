import sqlite3
import os
from flask import g, current_app

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'safesack360.db')
SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')


def get_db():
    """Get or create SQLite connection for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize database from schema.sql."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def query_db(query, args=(), one=False):
    """Query the database and return results as sqlite3.Row or list of Rows."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=(), commit=True):
    """Execute an INSERT/UPDATE/DELETE and return lastrowid."""
    db = get_db()
    cur = db.execute(query, args)
    if commit:
        db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id


def log_status_event(bag_id, status, user_id, note=None):
    """Record a lifecycle status event for chain of custody."""
    try:
        db = get_db()
        db.execute(
            """INSERT INTO status_events (bag_id, status, user_id, note)
               VALUES (?, ?, ?, ?)""",
            (bag_id, status, user_id, note)
        )
        db.commit()
    except Exception as e:
        print(f"[ERROR] Failed to log status event: {e}")


def audit(user_id, action, target, details=None):
    """Log an audit entry for security and compliance tracking."""
    try:
        db = get_db()
        db.execute(
            """INSERT INTO audit_log (user_id, action, target, details)
               VALUES (?, ?, ?, ?)""",
            (user_id, action, target, details)
        )
        db.commit()
    except Exception as e:
        print(f"[ERROR] Failed to write audit log: {e}")


def get_setting(key, default=None):
    """Retrieve a configuration value from system_settings."""
    try:
        row = query_db("SELECT value FROM system_settings WHERE key = ?", (key,), one=True)
        return row['value'] if row else default
    except Exception:
        return default


def set_setting(key, value):
    """Insert or update a configuration value in system_settings."""
    try:
        execute_db(
            """INSERT INTO system_settings (key, value, updated_at)
               VALUES (?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP""",
            (key, str(value))
        )
        return True
    except Exception as e:
        print(f"[ERROR] Failed to set setting {key}: {e}")
        return False
