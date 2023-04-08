from django.db import models

LIMIT_NAME = 256
LIMIT_SLUG = 50


class Category(models.Model):
    name = models.CharField('Категория', max_length=LIMIT_NAME)
    slug = models.SlugField(
        'Ссылка категории', unique=True, max_length=LIMIT_SLUG)

    class Meta:
        default_related_name = 'category'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=LIMIT_NAME)
    slug = models.SlugField(
        'Ссылка жанра', unique=True, max_length=LIMIT_SLUG)

    class Meta:
        default_related_name = 'genre'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=LIMIT_NAME,
        help_text='Название произведения')
    year = models.PositiveIntegerField(
        'Год выпуска произведения',
        help_text='Год выпуска произведения')
    rating = models.PositiveIntegerField(null=True, default=None)
    description = models.TextField(
        'Описание',
        help_text='Описание произведения',
        blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
        help_text='Жанр произведения',)
    category = models.ForeignKey(
        Category,
        verbose_name='Slug категории',
        help_text='Категория произведения',
        on_delete=models.SET_NULL,
        null=True,
        blank=False)
    rating = models.IntegerField(
        "Рейтинг", null=True, default=None)

    class Meta:
        default_related_name = 'title'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_name_category'
            )
        ]

    def __str__(self):
        return self.name


class Comment(models.Model):
    ...


class Review(models.Model):
    ...


class User(models.Model):
    ...
