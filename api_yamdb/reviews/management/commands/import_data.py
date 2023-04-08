from csv import DictReader

from django.core.management.base import BaseCommand

# from reviews.models import Category, Genre, Title, Comment, Review, User
from reviews.models import Category, Genre, Title


DATA = {
    'category': lambda x: Category(name=x['name'], slug=x['slug']),
    'genre': lambda x: Genre(name=x['name'], slug=x['slug']),
    'titles': lambda x: Title(
        name=x['name'],
        year=x['year'],
        category=Category.objects.get(id=x['category'])),
    # 'comments': lambda x: Comment(
    #     review_id=Review.objects.get(id=x['review_id']),
    #     text=x['text'],
    #     author=x['author'], pub_date=x['pub_date']),
    # 'genre_title': lambda x: print(x['title_id'], x['genre_id']),
    # 'review': lambda x: Review(
    #     title_id=Title.objects.get(id=x['title_id']),
    #     text=x['text'],
    #     author=x['author'],
    #     score=x['score'],
    #     pub_date=x['pub_date']),
    # 'users': lambda x: User(
    #     username=x['username'],
    #     email=x['email'],
    #     role=x['role'],
    #     bio=x['bio'],
    #     first_name=x['first_name'],
    #     last_name=x['last_name']),
}


class Command(BaseCommand):
    help = 'Import data from csvfile into the database'

    def handle(self, *args, **options):
        for filename, model in DATA.items():
            with open(f'static/data/{filename}.csv',
                      newline='', encoding='utf-8') as file:
                reader = DictReader(file)
                for row in reader:
                    model(row)
