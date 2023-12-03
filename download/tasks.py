import os
import re
from celery.utils.log import get_task_logger
from celery import shared_task
from pytube import YouTube

logger = get_task_logger(__name__)

@shared_task
def download_video(url):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    filename = video.default_filename
    download_path = os.path.join(os.getcwd(), 'download', filename)
    video.download(output_path=os.path.dirname(download_path))

    return filename
