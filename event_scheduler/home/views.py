from django.shortcuts import render
from booking.models import Event
from datetime import datetime, timedelta

def home_view(request):
    now = datetime.now()
    featured_events = Event.objects.filter(is_featured=True)[:4]
    upcoming_events = Event.objects.filter(
        date__gte=now
    ).order_by('date')[:6]
    
    return render(request, 'home/index.html', {
        'featured_events': featured_events,
        'upcoming_events': upcoming_events
    })