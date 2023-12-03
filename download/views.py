from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper
from pytube import YouTube
import os

def index(request):
    return render(request, "index.html")

# post request called download
def download(request):
    if request.method == "POST":
        url = request.POST.get("url")
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        filename = video.default_filename
        video.download()

        # Wrap the file in FileWrapper
        wrapper = FileWrapper(open(filename, 'rb'))
        response = HttpResponse(wrapper, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(filename)}'
        return response

    return render(request, "index.html")