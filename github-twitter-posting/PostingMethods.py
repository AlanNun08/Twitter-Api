import os
from datetime import datetime
import SqlCommands as sq


# Get the current date and time
def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def pathToClips(type):
    
    while True:
        # this functin needs to post the clip and then add it to sql
        path = input("Enter clip path: ")


        # Check the path to the clips is properly add by the user input
        if "D:\Cool-Programs\twitter_posting\clips_to_post" or "C:" in path:
            
            if type == 'Faze':
                times = 0
                while 2 > times:
                    times = times + 1

                    # Extract the filename from the path
                    filename = os.path.basename(path)  # 'Spectre   2024-09-09 03-51-21.mp4'

                    # Remove the file extension
                    clip_name = os.path.splitext(filename)[0]  # 'Spectre   2024-09-09 03-51-21'

                    # Get date and time
                    date_and_time = get_current_datetime()

                    # Create a dictionary with key-value pairs
                    clip_data = {
                        'clip_name': clip_name,
                        'date_inserted_into_database': date_and_time,
                        'path_to_clip': path,
                        'type': type
                    }

                    sq.insertComputerCaptureClipToDatabase(clip_data)

            return path
        else:
            print("Invalid path. Try again.")
            print("")
