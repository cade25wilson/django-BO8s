from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import download_video
from .models import Video
import os
import re

def index(request):
    return render(request, "index.html")

@csrf_exempt
def videos(request):
    if request.method == "POST":
        url = request.POST.get("url")
        download_video.delay(url)

    videos = Video.objects.values('filename', 'title').distinct()
    return render(request, "videos.html", {"videos": videos})

def get_video(request):
    file = request.GET.get('filename')
    file = Video.objects.filter(title=file).first()
    if file is None:
        return HttpResponse('File not found', status=404)
    file_path = os.path.join(os.getcwd(), 'download/download', file.filename)
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='video/mp4')
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
    return response