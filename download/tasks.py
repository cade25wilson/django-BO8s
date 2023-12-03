from celery.utils.log import get_task_logger
from celery import shared_task
from .models import Video
from pytube import YouTube
from celery.exceptions import SoftTimeLimitExceeded
import os

logger = get_task_logger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def download_video(self, url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        filename = yt.title
        download_path = os.path.join(os.getcwd(), 'download/download', filename)
        video.download(output_path=os.path.dirname(download_path))
        # make a title variable that removes all spaces and replaces them with underscores
        # this will be used to name the file
        filename = filename + '.mp4'
        # videotitle = re.sub('\s', '_', filename1)
        video = Video(filename=filename, title=filename)
        video.save()

        return filename
    except SoftTimeLimitExceeded:
        self.retry(countdown=60)  # retry in 60 seconds