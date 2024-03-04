from sql.queries import sql_execute


def create_initial_db():
    # create a table videos with the following columns: video_id, path, name, duration, program_name, leo_category, level
    sql_execute("""
    CREATE TABLE if not exists videos (
    video_id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL UNIQUE,
    name TEXT,
    duration REAL,
    program_name TEXT,
    leo_category TEXT,
    leo_level integer
    );
    """)

