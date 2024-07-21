from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    songWriters = models.CharField(max_length=255)
    year = models.IntegerField()
    genre = models.CharField(max_length=255)
