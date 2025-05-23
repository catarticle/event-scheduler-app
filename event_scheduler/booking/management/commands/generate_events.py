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
        fake_ru = Faker('ru_RU')  # Русскоязычный Faker
        fake_en = Faker() # Данные на английском
        
        RUSSIAN_CITIES = [
            'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань',
            'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону',
            'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 'Волгоград'
        ]
        
        # Категории мероприятий 
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
        venue_capacities = [50, 100, 150, 200, 300, 500, 800, 1000]
        for i in range(8):
            city = random.choice(RUSSIAN_CITIES)
            venue = Venue.objects.create(
                name=f"{city}, {random.choice(['Hall', 'Arena', 'Center', 'Theater'])}",
                address=f"{city}, {fake_ru.street_address()}",
                city=city, 
                capacity=random.choice(venue_capacities),
                photo='venues/venue_default.jpg'
            )
            venues.append(venue)
            self.stdout.write(f"Created venue: {venue.name} (Capacity: {venue.capacity})")
            
        # Генерация мероприятий с учетом мест
        for category_code, category_name in CATEGORIES:
            for i in range(random.randint(3, 5)):
                venue = random.choice(venues)
                
                # Создаем мероприятие с количеством мест
                event = Event.objects.create(
                title=self.generate_event_title(category_code, fake_en),
                venue=venue,
                date=fake_ru.future_datetime(end_date="+30d"),
                price=random.randint(500, 5000),
                description=self.generate_event_description(category_code, fake_ru),
                photo=random.choice(event_images) if event_images else None,
                is_featured=random.choice([True, False]),
                category=category_code,
                available_seats=venue.capacity,
                rating=round(random.uniform(3.0, 5.0), 1)  # Рейтинг от 3.0 до 5.0 с одним знаком после запятой
            )
                     
                
                
                self.stdout.write(
                    f"Created event: {event.title} at {event.venue.name} "
                    f"({event.available_seats}/{event.venue.capacity} seats available)"
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {Event.objects.count()} events')
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
        """Генерация связного тематического описания"""
        fake = Faker()
        templates = {
            'MUSIC': [
                {
                    'intro': "Грандиозное музыкальное событие этого сезона!",
                    'details': [
                        "В программе: выступления лучших исполнителей в стиле {style}.",
                        "Главные участники: {artist1} и {artist2}.",
                        "Особый гость: {headliner}.",
                        "Продолжительность: {hours} часов живой музыки."
                    ],
                    'ending': "Не пропустите этот незабываемый вечер великолепной музыки!"
                },
                {
                    'intro': "Международный фестиваль {style} музыки.",
                    'details': [
                        "Участвуют артисты из {country1} и {country2}.",
                        "Более {artists} исполнителей на {stages} сценах.",
                        "Также запланированы мастер-классы и джем-сейшены."
                    ],
                    'ending': "Билеты уже в продаже, количество мест ограничено!"
                }
            ],
            'SPORT': [
                {
                    'intro': "Крупнейшее спортивное событие года!",
                    'details': [
                        "Турнир по {sport} с участием команд из {country1} и {country2}.",
                        "Призовой фонд составляет {prize} рублей.",
                        "Судья мероприятия: {referee}.",
                        "Трансляция на {channel}."
                    ],
                    'ending': "Не упустите шанс увидеть лучших спортсменов в действии!"
                },
                {
                    'intro': "Профессиональные соревнования по {sport}.",
                    'details': [
                        "Участвуют чемпионы {league}.",
                        "Новичок сезона: {newcomer}.",
                        "Авторитетное жюри: {judge1} и {judge2}."
                    ],
                    'ending': "Накал страстей и зрелищные моменты гарантированы!"
                }
            ],
            'ART': [
                {
                    'intro': "Уникальная художественная выставка.",
                    'details': [
                        "Представлено {works} работ в стиле {style}.",
                        "Авторы: {artist1}, {artist2} и другие.",
                        "Куратор: {curator}.",
                        "Экспозиция охватывает период с {year1} по {year2} год."
                    ],
                    'ending': "Редкая возможность увидеть эти произведения в одном месте!"
                },
                {
                    'intro': "Арт-проект.",
                    'details': [
                        "Участвуют {artists} современных художников.",
                        "Используются техники: {technique1} и {technique2}.",
                        "Специальный проект: {special_project}."
                    ],
                    'ending': "Выставка перевернет ваше представление об искусстве!"
                }
            ],
            'FOOD': [
                {
                    'intro': "Гастрономический фестиваль {cuisine} кухни.",
                    'details': [
                        "Участвуют шеф-повара: {chef1} и {chef2}.",
                        "Дегустация {dishes} блюд.",
                        "Мастер-классы по {technique}.",
                        "Специальные гости из {country}."
                    ],
                    'ending': "Рай для гурманов и ценителей вкуса!"
                },
                {
                    'intro': "Фестиваль еды.",
                    'details': [
                        "Более {vendors} ресторанов и кафе.",
                        "Новые тренды: {trend1}, {trend2}.",
                        "Конкурс на лучшее блюдо с призом {prize} рублей."
                    ],
                    'ending': "Приходите голодными - уходить будете в восторге!"
                }
            ],
            'TECH': [
                {
                    'intro': "Главная технологическая конференция года.",
                    'details': [
                        "Тема: {topic}.",
                        "Спикеры: {speaker1} (компания {company1}) и {speaker2}.",
                        "Новые разработки в области {field}.",
                        "Интерактивные демо-зоны."
                    ],
                    'ending': "Узнайте будущее технологий первыми!"
                },
                {
                    'intro': "Хакатон '{theme}'.",
                    'details': [
                        "Призовой фонд: {prize} рублей.",
                        "Технологии: {tech1}, {tech2}.",
                        "Эксперты: {expert1} и {expert2}.",
                        "Формат: {format}."
                    ],
                    'ending': "48 часов кодинга, адреналина и инноваций!"
                }
            ],
            'BUSINESS': [
                {
                    'intro': "Бизнес-форум.",
                    'details': [
                        "Ключевые темы: {topic1}, {topic2}.",
                        "Спикеры: CEO {company1} и {company2}.",
                        "Кейсы из практики ведущих компаний.",
                        "Нетворкинг с {participants} участниками."
                    ],
                    'ending': "Инсайты, которые изменят ваш бизнес!"
                },
                {
                    'intro': "Профессиональный семинар с участием известных бизнесменов.",
                    'details': [
                        "Ведущий: {speaker1}, автор книги '{book}'.",
                        "Разберем: {case1}, {case2}.",
                        "Практические инструменты для {goal}.",
                        "Разбор реальных кейсов."
                    ],
                    'ending': "Примените эти знания уже завтра!"
                }
            ]
        }

        # Данные для подстановки
        placeholders = {
            # Музыка
            'style': random.choice(['рок', 'поп', 'джаз', 'электронной', 'классической', 'фолк']),
            'artist1': fake.last_name(),
            'artist2': fake.last_name(),
            'headliner': f"{fake.last_name()} Band",
            'country1': fake.country(),
            'country2': fake.country(),
            'hours': random.randint(3, 12),
            'stages': random.randint(1, 5),
            'artists': random.randint(10, 50),
            
            # Спорт
            'sport': random.choice(['футболу', 'хоккею', 'баскетболу', 'теннису', 'волейболу']),
            'prize': f"{random.randint(100, 5000)} тысяч" if random.choice([True, False]) else f"{random.randint(1, 5)} миллиона",
            'referee': f"{fake.last_name()}, {fake.country()}",
            'channel': random.choice(['НТВ', 'Матч ТВ', 'Eurosport', 'YouTube']),
            'league': random.choice(['лиги чемпионов', 'национальной сборной', 'премьер-лиги']),
            'newcomer': fake.last_name(),
            'judge1': f"{fake.last_name()}, {fake.job()}",
            'judge2': f"{fake.last_name()}, {fake.job()}",
            
            # Искусство
            'works': random.choice(['более 50', 'свыше 100', 'около 30']),
            'style': random.choice(['модернизм', 'импрессионизм', 'авангард', 'концептуальное искусство']),
            'curator': f"{fake.last_name()}, {fake.job()}",
            'year1': random.randint(1900, 2020),
            'year2': random.randint(2021, 2023),
            'theme': fake.catch_phrase(),
            'artists': random.randint(5, 20),
            'technique1': random.choice(['акварель', 'масло', 'графика']),
            'technique2': random.choice(['инсталляция', 'перформанс', 'цифровое искусство']),
            'special_project': fake.catch_phrase(),
            
            # Еда
            'cuisine': random.choice(['итальянской', 'японской', 'русской', 'французской']),
            'chef1': f"{fake.last_name()} ({fake.country()})",
            'chef2': f"{fake.last_name()} ({fake.country()})",
            'dishes': random.randint(20, 100),
            'technique': random.choice(['су-вид', 'ферментации', 'молекулярной кухни']),
            'country': fake.country(),
            'vendors': random.randint(15, 60),
            'trend1': random.choice(['фермерские продукты', 'растительные альтернативы', 'суперфуды']),
            'trend2': random.choice(['нулевые отходы', 'местные ингредиенты', 'этнические рецепты']),
            
            # Технологии
            'topic': fake.catch_phrase(),
            'speaker1': f"{fake.last_name()}",
            'speaker2': f"{fake.last_name()}",
            'company1': fake.company(),
            'company2': fake.company(),
            'field': random.choice(['искусственного интеллекта', 'блокчейна', 'кибербезопасности']),
            'tech1': random.choice(['AI', 'VR', 'IoT']),
            'tech2': random.choice(['Blockchain', 'Big Data', '5G']),
            'expert1': f"{fake.last_name()} ({fake.job()})",
            'expert2': f"{fake.last_name()} ({fake.job()})",
            'format': random.choice(['онлайн', 'оффлайн', 'гибридный']),
            
            # Бизнес
            'theme': fake.catch_phrase(),
            'topic1': random.choice(['лидерство', 'инновации', 'управление']),
            'topic2': random.choice(['маркетинг', 'финансы', 'HR']),
            'participants': random.choice(['500+', 'более 1000', '200+']),
            'book': fake.catch_phrase(),
            'case1': fake.bs(),
            'case2': fake.bs(),
            'goal': random.choice(['увеличения продаж', 'оптимизации процессов', 'развития команды'])
        }

        # Выбираем случайный шаблон для категории
        template = random.choice(templates[category])
        
        # Собираем описание
        description = template['intro'].format(**placeholders) + " "
        
        for detail in template['details']:
            description += detail.format(**placeholders) + " "
        
        description += template['ending']
        
        return description