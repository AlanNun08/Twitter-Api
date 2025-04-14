import tkinter as tk
from tkinter import filedialog, simpledialog

def select_videos():
    return filedialog.askopenfilenames(title="Select Videos", filetypes=[("MP4 files", "*.mp4")])

def assign_caption(video_paths):
    captions = {}
    for path in video_paths:
        caption = simpledialog.askstring("Caption Input", f"Enter caption for:\n{path}")
        if caption:
            captions[path] = caption
    return captions
