from django.contrib import admin
from django.urls import path
from django.contrib.auth.urls import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', registration_view, name='registration'),
]
