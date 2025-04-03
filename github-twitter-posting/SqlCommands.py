from datetime import datetime
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)

def whatUploadPathToUse(path , date, account):
    
    updateUploadStatusForTwitterUpload(path, date, account)
    

def updateUploadStatusForTwitterUpload(clip_path, date, accounts):
    try:
        with sqlite3.connect('destination_database.db') as conn:
            cursor = conn.cursor()

            # Find the primary key from clips based on the path
            cursor.execute('''
                SELECT id
                FROM clips
                WHERE path_to_clip = ?
            ''', (clip_path,))
            
            result = cursor.fetchone()  # Fetch only one result
            
            if result:
                downloaded_video_id = result[0]  # Extract the ID from the tuple
                
                # Check current status in uploadStatus
                cursor.execute('''
                    SELECT has_it_been_posted_to_twitter
                    FROM uploadStatus
                    WHERE clip_id = ?
                ''', (downloaded_video_id,))
                
                status_result = cursor.fetchone()  # Fetch current status
                
                if status_result and status_result[0] == 1:
                    # Increment the clip_id (assuming increment is just adding 1)
                    new_clip_id = downloaded_video_id + 1
                    
                    # Update status with the new clip_id
                    sql_query = '''
                        UPDATE uploadStatus
                        SET
                            has_it_been_posted_to_twitter = 1,
                            twitter_upload_date = ?,
                            account = ?
                        WHERE clip_id = ?
                    '''
                    cursor.execute(sql_query, (date, accounts, new_clip_id))
                    print(f"Updated upload status for new clip ID: {new_clip_id} and account: {accounts}.")
                    print("")
                
                else:
                    # Proceed with regular update
                    sql_query = '''
                        UPDATE uploadStatus
                        SET
                            has_it_been_posted_to_twitter = 1,
                            twitter_upload_date = ?,
                            account = ?
                        WHERE clip_id = ?
                    '''
                    cursor.execute(sql_query, (date, accounts, downloaded_video_id))
                    print(f"Successfully updated upload status for clip ID: {downloaded_video_id} and account: {accounts}.")
                    print("")
                
                # Commit changes
                conn.commit()
            else:
                print(f"No matching clip ID found for path: {clip_path}.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
              

def insertComputerCaptureClipToDatabase(clip_data):

    try:
        # Connect to SQLite database
        conn = sqlite3.connect('destination_database.db')
        cursor = conn.cursor()

        # Insert tweet data into the table
        cursor.execute('''
            INSERT INTO clips (clip_name, date_inserted_into_database, path_to_clip, type)
            VALUES (?, ?, ?, ?)
        ''', (
            clip_data.get("clip_name"),
            clip_data.get("date_inserted_into_database"),
            clip_data.get("path_to_clip"),
            clip_data.get("type")
        ))

        # Commit changes
        conn.commit()

        # Get the id of the newly inserted row
        new_id = cursor.lastrowid
        
        # Insert to new_id to the uploadStatus table
        insertUploadStatusUsingClipId(new_id)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the connection is closed
        conn.close()

# Get the current date and time
def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getTweetDataForSql(url, path, tweet_id, whatAccountToUse):

    # Define the type
    type = whatAccountToUse

    # Extract the tweet ID
    tweet_id_to_sql = tweet_id

    # Find the start index of the username part
    username_index = url.find('x.com/') + len('x.com/')  # Skip '/'

    # Find the end index of the username part (before 'status/')
    username_end_index = url.find('/status/')

    # Extract the username
    username = url[username_index:username_end_index]

    # Get date and time
    date_and_time = get_current_datetime()

    # Path to SQL or Twitter clip
    path_to_sql = path

    # Create a dictionary with key-value pairs
    tweet_data = {
        'tweet_id': tweet_id_to_sql,
        'user_name': username,
        'date_and_time_inserted_into_database': date_and_time,
        'path_to_clip': path_to_sql,
        'type': type
    }
    return tweet_data

def insertUploadStatusUsingClipId(clip_id):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('destination_database.db')
        cursor = conn.cursor()

        # Define the SQL query with placeholders
        sql_query = '''
            INSERT INTO uploadStatus (
                downloaded_video_id,
                clip_id,
                has_it_been_posted_to_twitter,
                twitter_upload_date,
                has_it_been_posted_to_tiktok,
                tiktok_upload_date,
                has_it_been_posted_to_youtube_shorts,
                youtube_shorts_upload_date,
                has_it_been_posted_to_instagram,
                instagram_upload_date,
                has_it_been_posted_to_facebook_page,
                facebook_page_upload_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Default values for other columns
        default_values = (
            None,
            int(clip_id),  # Assuming clip_id is optional
            0,     # has_it_been_posted_to_twitter (default 0)
            None,  # twitter_upload_date (default None)
            0,     # has_it_been_posted_to_tiktok (default 0)
            None,  # tiktok_upload_date (default None)
            0,     # has_it_been_posted_to_youtube_shorts (default 0)
            None,  # youtube_shorts_upload_date (default None)
            0,     # has_it_been_posted_to_instagram (default 0)
            None,  # instagram_upload_date (default None)
            0,     # has_it_been_posted_to_facebook_page (default 0)
            None   # facebook_page_upload_date (default None)
        )

        # Execute the SQL query with the new ID and default values
        cursor.execute(sql_query, default_values)

        # Commit changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the connection is closed
        conn.close()