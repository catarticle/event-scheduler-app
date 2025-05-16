from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login  
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from booking.models import Event
from .models import THEME_CHOICES

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            user.bio = f"Интересы: {dict(THEME_CHOICES).get(form.cleaned_data['interests'])}"
            events = Event.objects.filter(category__in=user.interests)[:3]
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
    return render(request, 'users/profile.html')

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
    selected_categories = request.GET.getlist('category')  # Получаем список выбранных категорий
    
    if 'all' in selected_categories or not selected_categories:
        # Если выбрано "Все" или ничего не выбрано
        events = Event.objects.all()
    else:
        # Фильтруем по выбранным категориям
        events = Event.objects.filter(category__in=selected_categories)
    
    # Сортировка по дате (новые сначала)
    events = events.order_by('-date')[:12]
    
    return render(request, 'users/recommendations.html', {
        'events': events,
        'selected_categories': selected_categories,
        'theme_choices': dict(THEME_CHOICES)
    })