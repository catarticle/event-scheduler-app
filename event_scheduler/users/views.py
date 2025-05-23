from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login  
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from booking.models import Event, Venue
from django.db.models import Q
from .models import THEME_CHOICES

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            
            # Получаем список выбранных интересов
            selected_interests = form.cleaned_data['interests']
            
            # Преобразуем ключи в читаемые названия
            theme_dict = dict(THEME_CHOICES)
            interest_names = [theme_dict.get(interest, interest) for interest in selected_interests]
            
            # Формируем строку для bio
            user.bio = f"Интересы: {', '.join(interest_names)}"
            
            # Получаем рекомендации (первые 3 события по интересам)
            events = Event.objects.filter(category__in=selected_interests)[:3]
            
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    
    context = {
        'form': form,
        'theme_choices': dict(THEME_CHOICES)  
    }
    return render(request, 'users/registration.html', context)



@login_required
def profile(request):
    bookings = request.user.bookings.select_related('event').order_by('-created_at')
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def recommendations(request):
    selected_categories = request.GET.getlist('category')
    selected_ratings = request.GET.getlist('rating')
    selected_cities = request.GET.getlist('city')
    
    # Начинаем с базового QuerySet
    events = Event.objects.all()
    
    # Фильтрация по категориям
    if selected_categories and 'all' not in selected_categories:
        events = events.filter(category__in=selected_categories)
    
    # Фильтрация по рейтингу
    if selected_ratings:
        rating_filters = Q()
        for rating in selected_ratings:
            try:
                min_rating = float(rating)
                rating_filters |= Q(rating__gte=min_rating)
            except ValueError:
                continue
        events = events.filter(rating_filters)
        
    # Фильтрация по городам
    if selected_cities:
        events = events.filter(venue__city__in=selected_cities)
    
    # Сортировка и ограничение
    events = events.order_by('-date')[:12]
    
    # Получаем список всех городов, где есть мероприятия
    available_cities = Venue.objects.values_list('city', flat=True).distinct()
    
    # Подготовка контекста
    rating_choices = [
        ('4.5', '4.5+ ★★★★☆'),
        ('4.0', '4.0+ ★★★★☆'),
        ('3.5', '3.5+ ★★★☆☆'),
        ('3.0', '3.0+ ★★★☆☆'),
    ]
    
    return render(request, 'users/recommendations.html', {
        'events': events,
        'selected_categories': selected_categories,
        'selected_ratings': selected_ratings,
        'selected_cities': selected_cities,
        'theme_choices': dict(THEME_CHOICES),
        'rating_choices': rating_choices,
        'available_cities': available_cities,
    })