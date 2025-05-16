from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Регистрация
    path('registration/', views.registration, name='registration'),  
    
    # Вход/выход
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='users/login.html'
         ), 
         name='login'),
    
    path('logout/', 
         auth_views.LogoutView.as_view(
             template_name='users/logout.html'
         ), 
         name='logout'),
    
    # Профиль пользователя
    path('profile/', views.profile, name='profile'),  # Добавляем основной профиль
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # Добавляем редактирование профиля

    # Смена пароля
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             template_name='users/password_change.html'
         ),
         name='password_change'),
    
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'
         ),
         name='password_change_done'),
    
    path('recommendations/', views.recommendations, name='recommendations'),
]