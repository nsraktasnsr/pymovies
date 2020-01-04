from django.db import models
from movies import models as movieModel

# Create your models here.


class Comment(models.Model):

    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name='Kullanici')
    movie = models.ForeignKey(
        movieModel.Movie, on_delete=models.CASCADE, verbose_name='Movie')

    rating = models.CharField(max_length=50, verbose_name='Puan')
    comment = models.TextField(verbose_name='Yorum')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Olusturma Tarih')

    def __str__(self):
        return str(self.user)


class Message(models.Model):

    email = models.CharField(max_length=50, verbose_name='email')
    name = models.CharField(max_length=50, verbose_name='name')
    surname = models.CharField(max_length=50, verbose_name='surname')

    message = models.TextField(verbose_name='Message')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Date')

    def __str__(self):
        return str(self.email)
