from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length= 100, verbose_name="Movie Name")
    description = models.TextField(verbose_name="Details")
    turu = models.CharField(max_length=100, verbose_name="Category", default="" )
    yil = models.CharField(max_length=50, verbose_name="Year", default="")
    imdb = models.FloatField(max_length=50, verbose_name="Imdb", default ="")
    yonetmen = models.CharField(max_length=100, verbose_name="Director", default="")
    oyuncular = models.CharField(max_length=200, verbose_name="Cast", default="")
    fragman_link = models.CharField(max_length=100, verbose_name="Link", default="")
    image = models.CharField(max_length=50, verbose_name="Picture")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    isPublished = models.BooleanField(default = True)


    def __str__(self):
        return self.name

    def get_image_path(self):
        return '/img/' + self.image