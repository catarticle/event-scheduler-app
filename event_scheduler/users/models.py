from django.db import models
from django.contrib.auth.models import AbstractUser
import json

THEME_CHOICES = [
    ('MUSIC', '🎵 Музыкальные мероприятия'),
    ('SPORT', '⚽ Спортивные события'),
    ('ART', '🎨 Искусство и выставки'), 
    ('FOOD', '🍔 Гастрономические фестивали'),
    ('TECH', '💻 Технологии и наука'),
    ('BUSINESS', '💼 Бизнес-мероприятия'),
]

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    interests = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Предпочтения'
    )
    
    def add_interests_to_bio(self):
        if not self.interests:  # Проверяем, есть ли интересы
            return
        
        selected = []
        for interest in self.interests:
            label = dict(THEME_CHOICES).get(interest)
            if label:  # Добавляем только если label не None
                selected.append(label)
        
        if selected:  # Если есть что добавлять
            self.bio = f"Интересы: {', '.join(selected)}"

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'