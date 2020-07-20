from django.db import models

# Create your models here.
class FavoritesList(models.Model):
    pass

class Company(models.Model):
    favoritesList = models.ForeignKey('FavoritesList', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)

# class Candlestick(models.Model):
#     company = models.ForeignKey('Company', on_delete=models.CASCADE)
#     date = models.DateField()
#     open = models.DecimalField(max_digits=11, decimal_places=4)
#     high = models.DecimalField(max_digits=11, decimal_places=4)
#     low = models.DecimalField(max_digits=11, decimal_places=4)
#     close = models.DecimalField(max_digits=11, decimal_places=4)
#     volume = models.IntegerField()
