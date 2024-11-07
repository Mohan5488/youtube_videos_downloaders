from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
import os
from yt_dlp import YoutubeDL

# Create your views here.
def index(request):
    return render(request, 'youtube.html')

def downloader(request):
    if request.method == 'POST':
        channel_url = request.POST.get('channel_url')
        download_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
        os.makedirs(download_dir, exist_ok=True)
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([channel_url])
            
        video_files = os.listdir(download_dir)
        video_urls = [f"{settings.MEDIA_URL}downloads/{file}" for file in video_files]

        return render(request, 'downloaded_videos.html', {'video_urls': video_urls})
    
    return render(request, 'youtube.html',{'video_urls': video_urls})