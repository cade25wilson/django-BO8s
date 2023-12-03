from django.shortcuts import render
from django.http import FileResponse
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

        # Open the file in binary mode and return it as a response
        with open(filename, 'rb') as f:
            response = FileResponse(f, content_type='video/mp4')
            # Set the Content-Disposition header to make the browser treat the response as a file download
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(filename)}'
            return response

    return render(request, "index.html")