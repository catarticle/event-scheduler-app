from django.db import models
from django.templatetags.static import static

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    capacity = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='venues/', blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    # Категории мероприятий (должны совпадать с users.models.THEME_CHOICES)
    CATEGORY_CHOICES = [
        ('MUSIC', '🎵 Музыка'),
        ('SPORT', '⚽ Спорт'),
        ('ART', '🎨 Искусство'),
        ('FOOD', '🍔 Еда'),
        ('TECH', '💻 Технологии'),
        ('BUSINESS', '💼 Бизнес'),
    ]
    
    title = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='events/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='MUSIC',
        verbose_name='Категория'
    )

    def get_photo_url(self):
        """Возвращает URL фото или дефолтное изображение"""
        if self.photo:
            return self.photo.url
        return static('images/default_event.jpg')

    def get_category_display(self):
        """Возвращает читаемое название категории с иконкой"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_category_class(self):
        """Возвращает CSS-класс для категории (для стилизации)"""
        return self.category.lower()

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    class Meta:
        ordering = ['date']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'