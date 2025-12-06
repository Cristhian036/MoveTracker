from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('live/', views.live_camera, name='live_camera'),
    path('live_feed/', views.live_feed, name='live_feed'),
    path('upload/', views.upload_video, name='upload_video'),
    path('uploaded_feed/<str:filename>/', views.uploaded_video_feed, name='uploaded_video_feed'),
    path('get_latest_plate/', views.get_latest_plate, name='get_latest_plate'),
    path('delete_video/<str:filename>/', views.delete_video, name='delete_video_file'),
]
