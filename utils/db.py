import sqlite3

def create_table():
    conn = sqlite3.connect('storage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            token TEXT PRIMARY KEY,
            language TEXT NOT NULL,
            stdout TEXT,
            stderr TEXT,
            webhook TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()


def add_new_submission(id,language,webhook = ""):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO submissions (token, language,webhook) VALUES (?, ?)",
        (id,language,webhook)
      )
    conn.commit()
    conn.close()

def get_submissions(ids: str):
    conn = sqlite3.connect("storage.db")
    conn.row_factory = sqlite3.Row  # lets us access rows like dicts
    cursor = conn.cursor()

    try:
        # Split the semicolon-separated IDs
        id_list = [x.strip() for x in ids.split(";") if x.strip()]

        if not id_list:
            print("⚠️ No IDs provided.")
            return []

        # Build placeholders dynamically
        placeholders = ",".join(["?"] * len(id_list))
        query = f"SELECT token,stdout,stderr FROM submissions WHERE token IN ({placeholders})"

        cursor.execute(query, id_list)

        # Convert each row to a dict
        rows = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return rows

    except Exception as e:
        print("Error fetching submissions:", e)
        conn.close()
        return []

    
def update_submission_output(id: str, stdout: str, stderr: str):
    try:
        conn = sqlite3.connect("storage.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE submissions
            SET stdout = ?, stderr = ?
            WHERE token = ?
            """,
            (stdout, stderr, id)
        )

        conn.commit()

        # Fetch the updated row
        cursor.execute("SELECT * FROM submissions WHERE token = ?", (id,))
        row = cursor.fetchone()

        conn.close()
        if row:
            return dict(row)
        else:
            print(f"No submission found for token {id}")
            return None
    except Exception as e:
        print("Database update failed:", e)