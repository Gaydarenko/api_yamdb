from django.core.management.base import BaseCommand
from csv import DictReader

from reviews.models import Category, Genre, Title


MODELS = {
    'category': lambda x: print(x['name'], x['slug']),
    'comments': lambda x: print(x['review_id'], x['text'], x['author'], x['pub_date']),
    'genre': lambda x: print(x['name'], x['slug']),
    'genre_title': lambda x: print(x['title_id'], x['genre_id']),
    'review': lambda x: print(x['title_id'], x['text'], x['author'], x['score'], x['pub_date']),
    'titles': lambda x: print(x['name'], x['year'], x['category']),
    'users': lambda x: print(x['username'], x['email'], x['role'], x['bio'], x['first_name'], x['last_name']),
}


class Command(BaseCommand):
    help = 'write the filename without extension you want to import into the database'

    def handle(self, *args, **options):
        for key in MODELS:
            self.import_data(key)

    def import_data(self, data_name):
        with open(f'static/data/{data_name}.csv', newline='') as file:
            reader = DictReader(file)
            for row in reader:
                action = MODELS[data_name]
                action(row)
