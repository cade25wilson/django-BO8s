from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import download_video
import os
import re

def index(request):
    return render(request, "index.html")

# @csrf_exempt 

# def download(request):
#     if request.method == "POST":
#         url = request.POST.get("url")
#         yt = YouTube(url)
#         video = yt.streams.get_highest_resolution()
#         filename = video.default_filename
#         video.download()

#         # Wrap the file in FileWrapper
#         wrapper = FileWrapper(open(filename, 'rb'))
#         response = HttpResponse(wrapper, content_type='video/mp4')
#         response['Content-Length'] = os.path.getsize(filename)
#         response['Content-Disposition'] = f'attachment; filename={os.path.basename(filename)}'
#         return response

#     return render(request, "index.html")

@csrf_exempt
def download(request):
    if request.method == "POST":
        url = request.POST.get("url")
        download_video.delay(url)
        videos = os.listdir(os.path.join(os.getcwd(), 'download/download'))
        videos = [re.sub('\.mp4$', '', video) for video in videos]
        return render(request, "videos.html", {"message": "Video is being downloaded", "videos": videos})

    return render(request, "index.html")


def videos(request):
    videos = os.listdir(os.path.join(os.getcwd(), 'download/download'))
    # remove .mp4 extension
    videos = [re.sub('\.mp4$', '', video) for video in videos]
    return render(request, "videos.html", {"videos": videos})

def get_video(request):
    file = request.GET.get('filename')
    file = f'{file}.mp4'
    file_path = os.path.join(os.getcwd(), 'download/download', file)
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='video/mp4')
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
    return response