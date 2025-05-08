from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)
    df = models.IntegerField(default=0)  # Количество документов, содержащих это слово

    def __str__(self):
        return self.word

