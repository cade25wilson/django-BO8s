from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    # path('download/', views.download, name="download"),
    path('videos/', views.videos, name="videos"),
    path('downloadfile/', views.get_video, name="downloadfile"),
]