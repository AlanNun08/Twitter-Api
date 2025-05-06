import tweepy
import PostingMethods as pm
import SqlCommands as sq
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import cv2  # OpenCV to read video frames and generate thumbnails
import os

def getApi(tokens):
    auth = tweepy.OAuthHandler(tokens.get('consumer_api_key'), tokens.get('consumer_api_key_secret'))
    auth.set_access_token(tokens.get('access_token') ,tokens.get('access_token_secret'))
    return tweepy.API(auth, wait_on_rate_limit=True)

def getClient(tokens):

    client = tweepy.Client(bearer_token=tokens.get('bearer_token'), consumer_key=tokens.get('consumer_api_key'), consumer_secret=tokens.get('consumer_api_key_secret'), 
                           access_token=tokens.get('access_token'), access_token_secret=tokens.get('access_token_secret'), wait_on_rate_limit=True)
    return client

def postMediaToTwitter(tokens, filename, text):
    try:
        
        api = getApi(tokens)
        client = getClient(tokens)

        media_id = api.media_upload(filename=filename).media_id_string
        client.create_tweet(text=text, media_ids=[media_id])
        print("tweeted!")
        print("")
        return 1
    except:
        print("couldn't tweet")
        print("")
        return 0

def read_tokens_from_file():
    # Open the text file containing the information
    with open('Twitter Api Keys.txt', 'r') as file:
        lines = file.readlines()

    # Initialize the result dictionary
    accounts_info = {}

    # Temporary holders
    tokens = {}
    account_name = None

    # Process each line
    for line in lines:
        line = line.strip()

        # Start of a new account
        if "Twitter API Account" in line:
            if account_name is not None:
                accounts_info[account_name] = tokens

            # Extract account name after the dash
            account_name = line.split('-')[-1].strip()
            tokens = {}

        elif "Consumer API Key" in line:
            tokens['consumer_api_key'] = line.split(":")[1].strip()
        elif "Consumer API Secret" in line:
            tokens['consumer_api_key_secret'] = line.split(":")[1].strip()
        elif "Access Token" in line:
            tokens['access_token'] = line.split(":")[1].strip()
        elif "Access Token Secret" in line:
            tokens['access_token_secret'] = line.split(":")[1].strip()
        elif "Bearer Token" in line:
            tokens['bearer_token'] = line.split(":")[1].strip()

    # Add the last account's tokens
    if account_name is not None:
        accounts_info[account_name] = tokens

    return accounts_info

# Function to generate thumbnail from a video file
def generate_thumbnail(video_path):
    # Use OpenCV to extract a frame from the video
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()  # Read the first frame
    if ret:
        # Resize the frame to create a thumbnail
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert color from BGR to RGB
        image = Image.fromarray(frame)
        image = image.resize((100, 100), Image.Resampling.LANCZOS)

        cap.release()
        return ImageTk.PhotoImage(image)
    return None

# Function to create the GUI and select video files
def select_videos():
    # Path where the video files are stored
    folder_path = r'C:\Users\aa\Desktop\Cool-Programs\Twitter-Api\github-twitter-posting\Clips to post'
    
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' not found.")
        return
    
    # Get all video files in the folder
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    video_files = [f for f in os.listdir(folder_path) if any(f.endswith(ext) for ext in video_extensions)]
    
    if not video_files:
        print(f"No video files found in '{folder_path}'.")
        return
    
    # Set up the tkinter window
    root = tk.Tk()
    root.title("Select Videos")
    
    # Dictionary to store selected video paths
    selected_videos = {}

    # Function to update the dictionary with selected videos
    def save_selection():
        for index, var in enumerate(checkbox_vars):
            if var.get() == 1:  # If the checkbox is selected
                selected_videos[index] = os.path.join(folder_path, video_files[index])
        
        # Close the tkinter window
        root.quit()

    # Create a list to store the checkbox variables
    checkbox_vars = []

    # Create a frame to hold video thumbnails and checkboxes
    frame = tk.Frame(root)
    frame.pack()

    # Add checkboxes and thumbnails for each video file
    for i, video_file in enumerate(video_files):
        video_path = os.path.join(folder_path, video_file)
        
        # Generate thumbnail for the video
        thumbnail = generate_thumbnail(video_path)
        
        # Create a checkbox variable
        var = tk.IntVar()
        checkbox_vars.append(var)
        
        # Create a frame for each video with thumbnail and checkbox
        video_frame = tk.Frame(frame)
        video_frame.pack(anchor='w')
        
        # Display the thumbnail
        if thumbnail:
            thumbnail_label = tk.Label(video_frame, image=thumbnail)
            thumbnail_label.image = thumbnail  # Keep a reference to the image
            thumbnail_label.grid(row=0, column=0)
        
        # Add the checkbox for selection
        checkbox = tk.Checkbutton(video_frame, text=video_file, variable=var)
        checkbox.grid(row=0, column=1)

    # Add a button to save the selection
    save_button = tk.Button(root, text="Save Selection", command=save_selection)
    save_button.pack()

    # Start the tkinter event loop
    root.mainloop()

    return selected_videos

# Function to assign captions to selected videos
def assign_caption(videos_dict):
    # Check if videos are selected
    if not videos_dict:
        print("No videos selected. Please select videos first.")
        return
    
    # Dictionary to store video paths and their respective captions
    videos_with_captions = {}
    
    
    # Prompt the user for a caption for each video
    for video_path in videos_dict.values():
        caption = input(f"Enter Caption For Video: {video_path} : ")
        videos_with_captions[video_path] = caption
    
    # Return the dictionary with video paths and captions
    return videos_with_captions

# Get the current date and time
def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    while True:
        tokensFromSpecifiedAccount = read_tokens_from_file()
            
        path_to_selected_videos = select_videos()

        # If videos were selected, ask for the caption and assign it
        if path_to_selected_videos:
            videos_with_captions = assign_caption(path_to_selected_videos)
            

        # check if the captions work
        # create a gui for a computer program
        for path, caption in videos_with_captions.items():

            # Display available accounts
            for account_info in tokensFromSpecifiedAccount.items():
                print (f"Account: {account_info[0]}")
                print("")
                print("")

            # Prompt user to select an account
            account = input("Enter the account name to post to: ")
            tokens = tokens = tokensFromSpecifiedAccount[account]

            # assign the correct tokens to the postMediaToTwitter function
            status = postMediaToTwitter(tokens, path, caption)
            if status == 1:
                # use path to update sql
                # use path to get the downloadedtwittervideo id and then use the id to update the status table to check that 
                # it has been upload to twitter
                sq.whatUploadPathToUse(path, get_current_datetime(), tokensFromSpecifiedAccount.get(account))

if __name__ == '__main__':
    main()