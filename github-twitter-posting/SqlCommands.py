import sqlite3
from datetime import datetime

def create_clips_database():
    """
    Creates the database and clips table if it doesn't exist.
    """
    conn = sqlite3.connect(r"C:\Users\aa\Desktop\Cool-Programs\Twitter-Api\github-twitter-posting\database\clips.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        clip_path TEXT UNIQUE,
        uploaded_to_twitter INTEGER DEFAULT 0,
        twitter_upload_date TEXT,
        twitter_account TEXT
    );
    ''')

    conn.commit()
    conn.close()

def mark_clip_uploaded(clip_path, twitter_account):
    """
    Marks an existing clip in the database as uploaded to Twitter.
    Only works if clip_path already exists in the database.
    """
    conn = sqlite3.connect(r"C:\Users\aa\Desktop\Cool-Programs\Twitter-Api\github-twitter-posting\database\clips.db")
    cursor = conn.cursor()

    twitter_upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = '''
    UPDATE clips
    SET
        uploaded_to_twitter = 1,
        twitter_upload_date = ?,
        twitter_account = ?
    WHERE
        clip_path = ?;
    '''

    cursor.execute(sql, (twitter_upload_date, twitter_account, clip_path))
    conn.commit()

    if cursor.rowcount == 0:
        print(f"❌ No clip found for path: {clip_path}")
    else:
        print(f"✅ Marked '{clip_path}' as uploaded using account '{twitter_account}'.")

    conn.close()

