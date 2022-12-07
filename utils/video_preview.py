from django.conf import settings
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pathlib import Path
import os

def cut_video_preview(video_path):
    length = 20 #seconds

    media_dir = settings.MEDIA_ROOT
    temp_dir = media_dir + "preview_temp/" 
    temp_path = temp_dir + Path(video_path).name

    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    ffmpeg_extract_subclip(video_path, 0, length, temp_path)

    return temp_path

def clean_temp(temp_path):
    if os.path.exists(temp_path):
        os.remove(temp_path)