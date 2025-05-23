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
    # Категории мероприятий 
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
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    # total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(default=50)
    
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='MUSIC',
        verbose_name='Категория'
    )

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return static('images/default_event.jpg')

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_category_class(self):
        return self.category.lower()

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    class Meta:
        ordering = ['date']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        
     
class Booking(models.Model):
    user = models.ForeignKey(
        'users.User',  
        on_delete=models.CASCADE,  # Удалять брони при удалении пользователя
        related_name='bookings', 
        verbose_name="Пользователь"
    )
    
    event = models.ForeignKey(
        'booking.Event',  
        on_delete=models.CASCADE,  # Удалять брони при удалении мероприятия
        verbose_name="Мероприятие"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False) # Потом продолжить реализовывать отмену брони мероприятия
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата оплаты")
    
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-created_at']
       
        
    