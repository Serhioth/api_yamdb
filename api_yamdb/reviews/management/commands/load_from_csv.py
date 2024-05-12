from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

MODEL_TO_CSV = {
    User: 'static/data/users.csv',
    Genre: 'static/data/genre.csv',
    Category: 'static/data/category.csv',
    Title: 'static/data/titles.csv',
    GenreTitle: 'static/data/genre_title.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv'
}


class Command(BaseCommand):
    """Импортирует данные из csv файлов в БД."""

    help = 'Import data to database from .csv files'

    def handle(self, *args, **options):
        for model in MODEL_TO_CSV:
            objs = []
            for row in DictReader(open(MODEL_TO_CSV[model], encoding='utf8')):
                if 'category' in row:
                    row['category_id'] = row['category']
                    del row['category']
                if 'author' in row:
                    row['author_id'] = row['author']
                    del row['author']
                objs.append(model(**row))
            model.objects.bulk_create(objs)
