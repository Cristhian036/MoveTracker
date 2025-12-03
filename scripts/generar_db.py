import sqlite3
import os
import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
from django.core.management import call_command

def main():
    SQL_FILE = BASE_DIR / 'db.sql'
    DB_FILE = BASE_DIR / 'bd.sqlite3'

    if not SQL_FILE.exists():
        print(f"Error: {SQL_FILE} not found.")
        return

    # 1. Remove existing DB
    if DB_FILE.exists():
        print(f"Removing existing {DB_FILE}...")
        DB_FILE.unlink()

    # 2. Create DB from SQL
    print("Creating database from SQL...")
    conn = sqlite3.connect(str(DB_FILE))
    try:
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        print("Database created successfully from SQL.")
    except Exception as e:
        print(f"Error executing SQL script: {e}")
        conn.close()
        return
    
    conn.close()

    # 3. Initialize Django and Fake Migrations
    print("Initializing Django...")
    django.setup()

    print("Applying migrations...")
    try:
        # Fake 'user' app migrations because db.sql already contains the schema and data
        print("Faking 'user' migrations...")
        call_command('migrate', 'user', fake=True)

        # Run fake-initial for other apps
        print("Applying migrations for other apps (fake-initial)...")
        call_command('migrate', fake_initial=True)
        
        print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error applying migrations: {e}")

if __name__ == '__main__':
    main()
