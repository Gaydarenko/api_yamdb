from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256,
        help_text='Название произведения')
    # TODO ограничения цифры года
    year = models.PositiveIntegerField(
        'Год выпуска произведения',
        help_text='Год выпуска произведения')
    # TODO уточнить откуда rating
    # rating = models.PositiveIntegerField(null=True)
    description = models.TextField(
        'Описание',
        help_text='Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Жанр произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True)

    # def __str__(self):
    #     return self.description
