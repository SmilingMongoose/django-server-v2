from django.db import models

# Create your models here.
class Visitor(models.Model):
    entered_visitor_name = models.CharField(max_length=200)

    def __str__(self):
        return self.entered_visitor_name

    

class Ticker(models.Model):
    ticker_name = models.TextField(null=True)
    dates = models.TextField(null=True)
    price_open = models.TextField(null=True)
    price_high = models.TextField(null=True)
    price_low = models.TextField(null=True)
    price_close = models.TextField(null=True)
    volume = models.TextField(null=True)

    average_open = models.FloatField()
    average_close = models.FloatField()
    min_open = models.FloatField()
    max_close = models.FloatField()


    def __str__(self):
        return self.ticker_name