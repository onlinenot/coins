from django.db import models


class Coin(models.Model):
    symbol = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    coin_id = models.CharField(max_length=128)
    icon = models.CharField(max_length=500)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
