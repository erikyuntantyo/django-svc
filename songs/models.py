from bson import ObjectId
from django.db.models import CharField, IntegerField, Model


class Song(Model):
    _id = CharField(primary_key=True, default=ObjectId, editable=False, max_length=24)
    title = CharField(max_length=255)
    artist = CharField(max_length=255)
    album = CharField(max_length=255)
    songWriters = CharField(max_length=255)
    year = IntegerField()
    genre = CharField(max_length=255)
