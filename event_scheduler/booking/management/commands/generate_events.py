from django.core.management.base import BaseCommand
from booking.models import Venue, Event
from faker import Faker
import random
from datetime import datetime, timedelta
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    help = 'Generates synthetic events with random photos by categories'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Категории мероприятий (должны совпадать с users.models.THEME_CHOICES)
        CATEGORIES = [
            ('MUSIC', 'Музыка'),
            ('SPORT', 'Спорт'),
            ('ART', 'Искусство'),
            ('FOOD', 'Еда'),
            ('TECH', 'Технологии'),
            ('BUSINESS', 'Бизнес'),
        ]
        
        # Очистка старых данных
        Event.objects.all().delete()
        Venue.objects.all().delete()

        # Получаем список доступных фото
        photos_dir = Path(settings.MEDIA_ROOT) / 'events'
        event_images = [
            f'events/{f.name}' 
            for f in photos_dir.glob('*') 
            if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']
        ]

        # Площадки с тематикой
        venues = []
        for _ in range(8):
            venue = Venue.objects.create(
                name=fake.company() + " " + random.choice(["Hall", "Arena", "Center", "Theater"]),
                address=fake.address(),
                capacity=random.choice([100, 300, 500, 1000]),
                photo='venues/venue_default.jpg'
            )
            venues.append(venue)

        # Генерация мероприятий по категориям
        for category_code, category_name in CATEGORIES:
            # Генерируем 3-5 мероприятий для каждой категории
            for i in range(random.randint(3, 5)):
                event = Event.objects.create(
                    title=self.generate_event_title(category_code, fake),
                    venue=random.choice(venues),
                    date=fake.future_datetime(end_date="+30d"),
                    price=random.randint(500, 5000),
                    description=self.generate_event_description(category_code, fake),
                    photo=random.choice(event_images) if event_images else None,
                    is_featured=random.choice([True, False]),
                    category=category_code
                )
                
                # Делаем 1-2 мероприятия featured в каждой категории
                if i < 2 and not Event.objects.filter(is_featured=True, category=category_code).exists():
                    event.is_featured = True
                    event.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully generated events by categories')
        )

    def generate_event_title(self, category, fake):
        """Генерация тематического названия мероприятия"""
        titles = {
            'MUSIC': [
                f"Концерт {fake.last_name()}",
                f"{fake.city()} Music Fest",
                "Джазовый вечер с " + fake.last_name(),
                "Рок фестиваль " + fake.word().capitalize()
            ],
            'SPORT': [
                f"Чемпионат по {fake.word()}",
                f"Турнир {fake.city()}",
                f"Матч {fake.last_name()} vs {fake.last_name()}",
                "Спортивный фестиваль"
            ],
            'ART': [
                f"Выставка '{fake.word().capitalize()}'",
                f"Галерея {fake.last_name()}",
                "Арт-перформанс " + fake.word().capitalize(),
                "Фотовыставка " + fake.city()
            ],
            'FOOD': [
                f"Фестиваль {fake.word()} кухни",
                f"{fake.city()} Food Market",
                "Дегустация вин от " + fake.last_name(),
                "Кулинарный мастер-класс"
            ],
            'TECH': [
                f"Конференция {fake.word().capitalize()} Tech",
                f"Хакатон {fake.city()}",
                f"Лекция: {fake.sentence(nb_words=4)}",
                "Выставка технологий"
            ],
            'BUSINESS': [
                f"Форум {fake.word().capitalize()} Business",
                f"Семинар по {fake.word()}",
                f"Встреча {fake.company()}",
                "Бизнес-завтрак"
            ]
        }
        return random.choice(titles[category])

    def generate_event_description(self, category, fake):
        """Генерация тематического описания"""
        descriptions = {
            'MUSIC': [
                f"Незабываемый музыкальный вечер с участием лучших исполнителей в стиле {fake.word()}. "
                f"В программе: {fake.sentence(nb_words=8)}",
                f"Грандиозный фестиваль в {fake.city()} с участием международных звезд. "
                f"{fake.paragraph(nb_sentences=2)}"
            ],
            'SPORT': [
                f"Спортивное мероприятие с участием команд {fake.country()} и {fake.country()}. "
                f"{fake.paragraph(nb_sentences=2)}",
                f"Турнир по {fake.word()} с призовым фондом {random.randint(100000, 1000000)} рублей. "
                f"{fake.sentence()}"
            ],
            'ART': [
                f"Уникальная выставка, представляющая работы художников из {fake.country()}. "
                f"{fake.paragraph(nb_sentences=2)}",
                f"Экспозиция включает {random.randint(20, 100)} работ в стиле {fake.word()}. "
                f"{fake.sentence()}"
            ],
            'FOOD': [
                f"Гастрономический праздник с участием шеф-поваров {fake.country()} кухни. "
                f"{fake.paragraph(nb_sentences=2)}",
                f"Дегустация более {random.randint(10, 50)} сортов {fake.word()}. "
                f"{fake.sentence()}"
            ],
            'TECH': [
                f"Передовые технологии в области {fake.word()}. Доклады от ведущих специалистов. "
                f"{fake.paragraph(nb_sentences=2)}",
                f"Практические мастер-классы по {fake.word()} и {fake.word()}. "
                f"{fake.sentence()}"
            ],
            'BUSINESS': [
                f"Бизнес-форум с участием CEO {fake.company()}. Темы: {fake.word()}, {fake.word()}, {fake.word()}. "
                f"{fake.paragraph(nb_sentences=2)}",
                f"Семинар по эффективному {fake.word()} в бизнесе. Практические кейсы. "
                f"{fake.sentence()}"
            ]
        }
        return random.choice(descriptions[category])