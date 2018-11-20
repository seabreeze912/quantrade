from django.db import models

# Create your models here.


class BtcDailyData(models.Model):
    close = models.FloatField(max_length=30)
    dateTime = models.DateTimeField(unique=True)
    high = models.FloatField(max_length=30)
    low = models.FloatField(max_length=30)
    open = models.FloatField(max_length=30)
    symbol = models.CharField(max_length=20)
    vol = models.FloatField(max_length=30)

    @classmethod
    def create_btc_daily_data(cls, close, dateTime, high, low, open, symbol, vol):
        data = cls(close=close, dateTime=dateTime, high=high, low=low, open=open, symbol=symbol, vol=vol)
        return data

