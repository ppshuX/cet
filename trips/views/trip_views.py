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
    """三岔河一日游页面 - 重定向到新的旅行计划"""
    from django.shortcuts import redirect
    from ..models.trip import Trip
    
    # 尝试查找对应 slug 的旅行计划
    try:
        trip = Trip.objects.filter(slug='trip1').first()
        if trip:
            # 重定向到新的旅行计划URL
            return redirect(f'/trip/{trip.slug}/', permanent=True)
    except Exception:
        pass
    
    # 如果找不到，重定向到首页
    return redirect('/', permanent=False)


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

