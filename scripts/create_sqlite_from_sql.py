import sqlite3
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
SQL_FILE = BASE / 'db.sql'
DB_FILE = BASE / 'db.sqlite3'

if not SQL_FILE.exists():
    print('db.sql not found at', SQL_FILE)
    sys.exit(1)

sql = SQL_FILE.read_text(encoding='utf-8')

if DB_FILE.exists():
    print('Removing existing', DB_FILE)
    DB_FILE.unlink()

conn = sqlite3.connect(str(DB_FILE))
try:
    cur = conn.cursor()
    print('Executing SQL script...')
    cur.executescript(sql)
    conn.commit()
    print('Database created at', DB_FILE)
    # print tables summary
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [r[0] for r in cur.fetchall()]
    print('Tables:', tables)
except Exception as e:
    print('Error executing SQL:', e)
    if DB_FILE.exists():
        print('Removing partially-created DB')
        DB_FILE.unlink()
    raise
finally:
    conn.close()
