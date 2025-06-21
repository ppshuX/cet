from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Comment, SiteStat
from django.utils import timezone
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def listening(request):
    return render(request, 'listening.html')

def reading(request):
    return render(request, 'reading.html')

def writing(request):
    return render(request, 'writing.html')

def translate(request):
    return render(request, 'translate.html')


def trip_page(request):
    stats, _ = SiteStat.objects.get_or_create(id=1)
    stats.views += 1
    stats.save()
    comments = Comment.objects.order_by('-timestamp')
    return render(request, 'cetapp/trip.html', {
        'comments': comments,
        'stats': stats,
    })

@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content').strip()
        if content:
            Comment.objects.create(content=content, is_owner=True)
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status': 'fail'})

@csrf_exempt
def like_view(request):
    stats = SiteStat.objects.get(id=1)
    stats.likes += 1
    stats.save()
    return JsonResponse({'likes':stats.likes})

@csrf_exempt
def checkin_view(request):
    stats = SiteStat.objects.get(id=1)
    stats.checked_in = True
    stats.save()
    return JsonResponse({'checked_in':True})
