import os

from research.statistics_about_videos import get_video_duration
from sql.queries import sql_execute


def create_initial_db():
    # create a table videos with the following columns: video_id, path, name, duration, program_name, leo_category, level
    sql_execute("""
    CREATE TABLE if not exists videos (
    video_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL UNIQUE,
    name TEXT,
    duration REAL,
    program_name TEXT
    );
    """)

    # create table exercies
    sql_execute("""
    CREATE TABLE if not exists exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_name TEXT NOT NULL UNIQUE,
    default_categories TEXT,
    default_level INTEGER,
    video_id INTEGER,
    FOREIGN KEY (video_id) REFERENCES videos (video_id)    
    );
    """)

    # create table exercise_categories
    sql_execute("""
    CREATE TABLE if not exists exercise_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
    );
    """)


def fill_video_meta_data():
    directory_path = "../data/short_videos/all"
    video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4')]
    # list_of_durations = []

    for i, video_file in enumerate(video_files):
        print(f"Processed video {i + 1}/{len(video_files)}: {video_file}")
        video_file_path = os.path.join(directory_path, video_file)
        duration_seconds = get_video_duration(video_file_path)
        possible_name = video_file.replace('.mp4', '')
        # print(possible_name.split('-'))
        possible_name = possible_name.split('-')[2]
        possible_name = possible_name.replace('_', ' ')
        if not possible_name.strip():
            possible_name = None
        print(f"Duration: {duration_seconds}, Name: {possible_name}, File: {video_file}")
        sql_execute("""INSERT INTO videos (file_name, name, duration)
                        VALUES (:file_name, :name, :duration);""",
                    file_name=video_file, name=possible_name, duration=duration_seconds)


if __name__ == '__main__':
    create_initial_db()
    # print("DB created")
    # fill_video_meta_data()

