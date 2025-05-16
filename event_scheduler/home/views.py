from django.shortcuts import render
from booking.models import Event
from datetime import datetime, timedelta

def home_view(request):
    now = datetime.now()
    
    # Рекомендуемые мероприятия (по категориям пользователя)
    recommended_events = []
    if request.user.is_authenticated and hasattr(request.user, 'interests'):
        recommended_events = Event.objects.filter(
            category__in=request.user.interests,
            date__gte=now
        ).order_by('date')[:4]
    
    # Если пользователь не авторизован или нет рекомендаций - показываем featured
    if not recommended_events:
        recommended_events = Event.objects.filter(
            is_featured=True,
            date__gte=now
        ).order_by('date')[:4]
    
    # Ближайшие мероприятия всех категорий
    upcoming_events = Event.objects.filter(
        date__gte=now
    ).exclude(
        id__in=[e.id for e in recommended_events]
    ).order_by('date')[:6]
    
    # Группировка по категориям для секции "По интересам"
    categories = {}
    if request.user.is_authenticated and hasattr(request.user, 'interests'):
        for category in request.user.interests:
            events = Event.objects.filter(
                category=category,
                date__gte=now
            ).order_by('date')[:3]
            if events:
                categories[category] = events
    
    return render(request, 'home/index.html', {
        'recommended_events': recommended_events,
        'upcoming_events': upcoming_events,
        'categories': categories,
        'now': now
    })