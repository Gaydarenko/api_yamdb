'''Import data from csv files to project DB'''
import csv
from reviews.models import Category, Genre, Title  # TODO write correct path


MOD_FILES = {
    # 'category': Category,
    'genre': Genre,
    # 'titles': Title
}

for name in MOD_FILES:
    with open(f'data/{name}.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(row)
            # category = MOD_FILES[name].objects.get_or_create(
            #     name=row[1],
            #     slug=row[2])
            # TODO уточнить тип category
