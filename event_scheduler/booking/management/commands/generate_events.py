from django.core.management.base import BaseCommand
from booking.models import Venue, Event
from faker import Faker
import random
from datetime import datetime, timedelta
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    help = 'Generates synthetic events with random photos'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Очистка старых данных
        Event.objects.all().delete()
        Venue.objects.all().delete()

        # 1. Получаем список доступных фото
        photos_dir = Path(settings.MEDIA_ROOT) / 'events'
        event_images = [
            f'events/{f.name}' 
            for f in photos_dir.glob('*') 
            if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']
        ]

        # 2. Создаем площадки
        venues = []
        for _ in range(5):
            venue = Venue.objects.create(
                name=fake.company() + " Hall",
                address=fake.address(),
                capacity=random.choice([100, 300, 500, 1000]),
                photo='venues/venue_default.jpg'  # Можно добавить фото для площадок
            )
            venues.append(venue)

        # 3. Генерируем мероприятия с фото
        for i in range(20):
            Event.objects.create(
                title=fake.sentence(nb_words=4),
                venue=random.choice(venues),
                date=fake.future_datetime(end_date="+30d"),
                price=random.randint(500, 5000),
                description=fake.paragraph(nb_sentences=3),
                photo=random.choice(event_images) if event_images else None,
                is_featured=random.choice([True, False])
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated 20 events with {len(event_images)} available photos')
        )