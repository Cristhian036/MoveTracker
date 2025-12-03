import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

# Setup paths
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
from django.core.management import call_command

def main():
    SQL_FILE = BASE_DIR / 'db.sql'
    DB_FILE = BASE_DIR / 'db.sqlite3'

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
    except Exception as e:
        print(f"Error executing SQL script: {e}")
        conn.close()
        return

    # 3. Fix Integrity Issues (Missing User and Tables)
    print("Checking data integrity and missing tables...")
    cursor = conn.cursor()
    
    # Create missing Django tables that are not in db.sql
    missing_tables_sql = [
        """CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);""",
        """CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");""",
        
        """CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);""",
        """CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");""",
        """CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");""",
        
        """CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);""",
        """CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");""",
        """CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");""",
        """CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");""",
        
        """CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);""",
        """CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");""",
        """CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");""",
        """CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");""",
        
        """CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);""",
        """CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");""",
        """CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");""",
        
        """CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);""",
        """CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");"""
    ]
    
    print("Creating missing standard Django tables...")
    for sql in missing_tables_sql:
        try:
            cursor.execute(sql)
        except Exception as e:
            print(f"Warning executing SQL: {e}")

    try:
        # Check if user with id=1 exists (referenced by parking_parkingconfiguration)
        cursor.execute("SELECT id FROM auth_user WHERE id=1")
        if not cursor.fetchone():
            print("Inserting default admin user (id=1) to satisfy foreign keys...")
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Columns based on db.sql: id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name, dni, phone
            # Password is 'admin' hashed with PBKDF2
            cursor.execute("""
                INSERT INTO auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name, dni, phone)
                VALUES (1, 'pbkdf2_sha256$720000$omKB5LQn9nxrg2rPcVHdO8$DpLI8VIQK3BWEJGvMLGiUO952EUY5vlitNIhT6freCQ=', NULL, 1, 'admin', 'User', 'admin@example.com', 1, 1, ?, 'Admin', NULL, NULL)
            """, (now,))
            conn.commit()
    except Exception as e:
        print(f"Warning during integrity check: {e}")
    
    conn.close()

    # 4. Initialize Django
    print("Initializing Django...")
    django.setup()

    # 5. Run Migrations
    print("Applying migrations...")
    try:
        # 1. Fake 'user' app migrations because db.sql already contains the schema and data (groups)
        # This prevents user.0002_create_user_groups from failing due to unique constraint
        print("Faking 'user' migrations...")
        call_command('migrate', 'user', fake=True)

        # 2. Run fake-initial for other apps
        # This will fake initial migrations for existing tables and apply others
        print("Applying migrations for other apps (fake-initial)...")
        call_command('migrate', fake_initial=True)
        
        print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error applying migrations: {e}")

if __name__ == '__main__':
    main()
