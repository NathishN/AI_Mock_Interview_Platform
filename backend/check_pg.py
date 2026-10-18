import psycopg

passwords = ["postgres", "admin", "root", "1234", "123456", "password", "interviewace"]

for pw in passwords:
    try:
        with psycopg.connect(f"host=localhost port=5432 user=postgres password={pw} dbname=postgres") as conn:
            print(f"SUCCESS with postgres:{pw}!")
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = 'interviewace'")
                if not cur.fetchone():
                    print("Creating database interviewace...")
                    cur.execute("CREATE DATABASE interviewace")
                cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'interviewace'")
                if not cur.fetchone():
                    print("Creating user interviewace...")
                    cur.execute("CREATE USER interviewace WITH PASSWORD 'interviewace'")
                else:
                    cur.execute("ALTER USER interviewace WITH PASSWORD 'interviewace'")
                cur.execute("GRANT ALL PRIVILEGES ON DATABASE interviewace TO interviewace")
            print("Successfully configured interviewace database & user!")
            break
    except Exception as e:
        pass
else:
    print("Could not connect with common passwords for postgres user.")
