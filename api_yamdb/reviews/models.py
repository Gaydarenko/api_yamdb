from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    #TODO as array
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(null=True)
    description = models.TextField()
    # TODO genre is array
    # genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, related_name='titles', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='titles', blank=True, null=True)

