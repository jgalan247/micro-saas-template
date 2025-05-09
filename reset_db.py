import os
import sqlite3

DB_PATH = "honestybox.db"
SCHEMA_PATH = "database/schema.sql"
SEED_PATH = "database/seed_data.sql"

def reset_database():
    # Step 1: Delete existing DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✅ Deleted existing {DB_PATH}")
    else:
        print(f"ℹ️ No existing {DB_PATH} to delete.")

    # Step 2: Create DB and run schema
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    print(f"✅ Created {DB_PATH} using {SCHEMA_PATH}")

    # Step 3: Seed DB
    with open(SEED_PATH, 'r') as f:
        conn.executescript(f.read())
    print(f"✅ Populated {DB_PATH} using {SEED_PATH}")

    # Step 4: Show tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("\n📦 Tables in database:", tables)

    # Step 5: Show contents of each table
    for table in tables:
        print(f"\n📄 Contents of table `{table}`:")
        try:
            cursor.execute(f"SELECT * FROM {table};")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("   (empty)")
        except Exception as e:
            print(f"   ⚠️ Error reading table `{table}`: {e}")

    conn.close()
    print("\n🎉 Reset complete.")

if __name__ == "__main__":
    reset_database()

