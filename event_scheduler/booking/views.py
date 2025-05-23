from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Event, Booking
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

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
    is_booked = False
    
    if request.user.is_authenticated:
        is_booked = Booking.objects.filter(event=event, user=request.user).exists()
    
    if request.method == 'POST' and 'booking' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        
        if is_booked: # Проверяем, не забронировал ли пользователь уже это мероприятие
            messages.error(request, "Вы уже забронировали это мероприятие.")
        elif not event.is_active or event.available_seats <= 0: # Проверяем доступность мероприятия
            messages.error(request, "Мероприятие недоступно для бронирования.")
        else:
            # Создаем бронь и уменьшаем количество мест
            try:
                with transaction.atomic():
                    Booking.objects.create(user=request.user, event=event)
                    event.available_seats -= 1
                    event.save()
                    messages.success(request, "Мероприятие успешно забронировано!")
                    is_booked = True  # Обновляем статус после бронирования
            except Exception as e:
                messages.error(request, f"Ошибка бронирования: {e}")
    
    return render(request, 'booking/event_detail.html', {
        'event': event,
        'is_booked': is_booked
    })
    
    
@require_POST
@login_required
@transaction.atomic
def process_payment(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_for_update(),
        id=booking_id,
        user=request.user
    )
    
    if booking.is_paid:
        messages.warning(request, "Это бронирование уже оплачено!")
        return redirect('profile')
    
    # Имитация оплаты
    booking.is_paid = True
    booking.payment_date = timezone.now()
    booking.save()
    
    messages.success(request, f"Оплата билета на {booking.event.title} прошла успешно!")
    return redirect('profile')