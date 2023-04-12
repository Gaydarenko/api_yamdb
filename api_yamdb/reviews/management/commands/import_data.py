from csv import DictReader

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

DATA = {
    'category': lambda x: Category.objects.create(
        id=x['id'], name=x['name'], slug=x['slug']),
    'genre': lambda x: Genre.objects.create(
        id=x['id'], name=x['name'], slug=x['slug']),
    'titles': lambda x: Title.objects.create(
        id=x['id'],
        name=x['name'],
        year=x['year'],
        category=Category.objects.get(id=x['category'])),
    'users': lambda x: User.objects.create(
        id=x['id'],
        username=x['username'],
        email=x['email'],
        role=x['role'],
        bio=x['bio'],
        first_name=x['first_name'],
        last_name=x['last_name']),
    'review': lambda x: Review.objects.create(
        id=x['id'],
        title=Title.objects.get(id=x['title_id']),
        text=x['text'],
        author=User.objects.get(id=x['author']),
        score=x['score'],
        pub_date=x['pub_date']),
    'comments': lambda x: Comment.objects.create(
        review=Review.objects.get(id=x['review_id']),
        text=x['text'],
        author=User.objects.get(id=x['author']),
        pub_date=x['pub_date']),
    # 'genre_title': lambda x: print(x['title_id'], x['genre_id']),
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
