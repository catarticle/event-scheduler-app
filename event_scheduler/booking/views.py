from django.shortcuts import render
from django.db.models import Q
from .models import Event

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'booking/event_list.html', {'events': events})

def search_view(request):
    query = request.GET.get('q', '')
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query))
    else:
        events = Event.objects.none()
    return render(request, 'booking/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'booking/event_detail.html', {'event': event})