from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

LIMIT_NAME = 256
LIMIT_SLUG = 50
CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='username', max_length=150, unique=True)
    email = models.EmailField(
        verbose_name='email address', max_length=254, unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=10, choices=CHOICES, default='user')

    @property
    def is_admin(self):
        "User ia admin?"
        return self.role == 'admin'

    @property
    def is_moderator(self):
        "User moderator?"
        return self.role == 'moderator'

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
        "Рейтинг", null=True, default=0)

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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
