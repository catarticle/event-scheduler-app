from django.urls import path
from . import views


urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('search/', views.search_view, name='search'),
    path('pay/<int:booking_id>/', views.process_payment, name='process_payment'),
]