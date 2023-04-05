from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256,
        help_text='Название произведения')
    year = models.PositiveIntegerField(
        'Год выпуска произведения',
        help_text='Год выпуска произведения')
    rating = models.PositiveIntegerField(null=True, default=None)
    description = models.TextField(
        'Описание',
        help_text='Описание произведения',
        blank=False
        )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Жанр произведения',
        # on_delete=models.SET_NULL,
        related_name='titles',
        blank=True
        )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория произведения',
        on_delete=models.CASCADE,
        related_name='titles',
        blank=True
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_name_category'
            )
        ]

    def __str__(self):
        return self.name
