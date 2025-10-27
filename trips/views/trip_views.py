"""
旅行页面相关视图
"""
from django.shortcuts import render
from ..models import Comment, SiteStat


def trip_page(request):
    """厦门旅行页面"""
    stats = SiteStat.objects.filter(page='trip').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip')
    stats.views += 1
    stats.save()
    comments = Comment.objects.filter(page='trip').order_by('-timestamp')
    return render(request, 'trips/trip.html', {
        'comments': comments,
        'stats': stats,
    })


def trip1(request):
    """三岔河一日游页面"""
    stats = SiteStat.objects.filter(page='trip1').first()
    if not stats:
        stats = SiteStat.objects.create(page='trip1')
    stats.views += 1
    stats.save()
    comments = Comment.objects.filter(page='trip1').order_by('-timestamp')
    return render(request, 'trips/trip1.html', {
        'comments': comments,
        'stats': stats,
    })


def trip2(request):
    """曲靖二日游页面"""
    return trip_page_generic(request, 'trip2')


def trip4(request):
    """长沙慢旅行页面"""
    return trip_page_generic(request, 'trip4')


def trip_page_generic(request, page_name):
    """通用旅行页面渲染函数"""
    stats = SiteStat.objects.filter(page=page_name).first()
    if not stats:
        stats = SiteStat.objects.create(page=page_name)
    stats.views += 1
    stats.save()
    comments = Comment.objects.filter(page=page_name).order_by('-timestamp')
    
    return render(request, f'trips/{page_name}.html', {
        'comments': comments,
        'stats': stats,
        'page_name': page_name,
    })

