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
    title = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='events/', blank=True)  # ImageField вместо CharField
    is_featured = models.BooleanField(default=False)

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return static('images/default_event.jpg')

    def __str__(self):
        return self.title