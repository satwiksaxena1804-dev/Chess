"""Saved-game storage used by both the game and the replay screen.

MySQL is the preferred backend, but it is optional: when the driver is not
installed, the server is unreachable, or the credentials are wrong, games are
stored in ``saves/games.json`` instead. That way saving and replaying work out
of the box for anyone who clones the repository.

Credentials are read from the environment (``.env``, see ``.env.example``) and
are never stored in the source code.
"""

import json
import os
from datetime import datetime

SAVES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
JSON_STORE = os.path.join(SAVES_DIR, "games.json")

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv is optional: plain environment variables work just as well.
    pass


def get_connection():
    """Open the project's MySQL database using local environment settings.

    The driver is imported lazily so the rest of the storage layer still works
    when mysql-connector-python is not installed.
    """
    import mysql.connector

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "chess"),
        connection_timeout=3,
    )


def _summarise(exc):
    """Turn an exception into a short single-line message."""
    text = str(exc).strip() or exc.__class__.__name__
    return " ".join(text.split())[:160]


# ----------------------------------------------------------------- MySQL ----
def _mysql_save(name, moves):
    """Insert or overwrite a game in MySQL. Raises on any failure."""
    conn = get_connection()
    try:
        cursor = conn.cursor(buffered=True)
        try:
            payload = json.dumps(moves)
            cursor.execute("SELECT id FROM chess_games WHERE name = %s", (name,))
            row = cursor.fetchone()
            if row:
                cursor.execute(
                    "UPDATE chess_games SET game_date = NOW(), moves_list = %s WHERE id = %s",
                    (payload, row[0]),
                )
                result = "updated"
            else:
                cursor.execute(
                    "INSERT INTO chess_games (name, game_date, moves_list) VALUES (%s, NOW(), %s)",
                    (name, payload),
                )
                result = "inserted"
            conn.commit()
            return result
        finally:
            cursor.close()
    finally:
        conn.close()


def _mysql_load(name):
    """Return the stored moves for a game, or None when MySQL has no such game."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT moves_list FROM chess_games WHERE name = %s", (name,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
        finally:
            cursor.close()
    finally:
        conn.close()


# ------------------------------------------------------- local JSON file ----
def _json_read():
    if not os.path.exists(JSON_STORE):
        return {}
    with open(JSON_STORE, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def _json_write(data):
    os.makedirs(SAVES_DIR, exist_ok=True)
    temporary = JSON_STORE + ".tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    os.replace(temporary, JSON_STORE)


def _json_save(name, moves):
    data = _json_read()
    existed = name in data
    data[name] = {
        "game_date": datetime.now().isoformat(timespec="seconds"),
        "moves": moves,
    }
    _json_write(data)
    return "updated" if existed else "inserted"


# ------------------------------------------------------------ public API ----
def save_game(name, moves):
    """Save a named game.

    Tries MySQL first and falls back to the local file. Returns
    ``(saved, message)`` where ``message`` is safe to show on screen.
    """
    if not name:
        return False, "No game name entered, nothing was saved."

    mysql_error = None
    try:
        _mysql_save(name, moves)
        return True, "Saved game '%s' to MySQL." % name
    except Exception as exc:  # missing driver, server down, bad credentials
        mysql_error = exc

    try:
        _json_save(name, moves)
        return True, "MySQL unavailable (%s). Saved game '%s' locally." % (
            _summarise(mysql_error),
            name,
        )
    except Exception as exc:
        return False, "Could not save game '%s' - MySQL: %s | local file: %s" % (
            name,
            _summarise(mysql_error),
            _summarise(exc),
        )


def load_game(name):
    """Load a named game.

    Checks MySQL first, then the local file, so games saved while MySQL was
    down are still found once it comes back. Returns ``(moves, message)``;
    ``moves`` is None when the game could not be loaded.
    """
    if not name:
        return None, "No game name entered."

    mysql_error = None
    try:
        moves = _mysql_load(name)
        if moves is not None:
            return moves, "Loaded game '%s' from MySQL." % name
    except Exception as exc:
        mysql_error = exc

    try:
        entry = _json_read().get(name)
    except Exception as exc:
        return None, "Could not load game '%s' - MySQL: %s | local file: %s" % (
            name,
            _summarise(mysql_error),
            _summarise(exc),
        )

    if entry is not None:
        moves = entry.get("moves") if isinstance(entry, dict) else entry
        return moves, "Loaded game '%s' from local saves." % name

    if mysql_error is not None:
        return None, "No saved game named '%s' (also could not reach MySQL: %s)." % (
            name,
            _summarise(mysql_error),
        )
    return None, "No saved game found with name '%s'." % name
