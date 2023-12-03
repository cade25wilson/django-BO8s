from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper
from celery import shared_task
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
import os

def index(request):
    return render(request, "index.html")

@csrf_exempt 

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
        return HttpResponse('Video is being downloaded')

    return render(request, "index.html")

@shared_task
def download_video(url):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    filename = video.default_filename
    video.download()

    # Wrap the file in FileWrapper
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='video/mp4')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(filename)}'
    return response