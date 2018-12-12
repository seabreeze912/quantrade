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


# *********策略3数据库*************
class BtcDifference(models.Model):
    ticker = models.CharField(max_length=30)
    exchangeName = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)
    open = models.FloatField(max_length=30)
    high = models.FloatField(max_length=30)
    low = models.FloatField(max_length=30)
    close = models.FloatField(max_length=30)
    vol = models.FloatField(max_length=30)
    dateTime = models.FloatField(max_length=30)

    @classmethod
    def create_btc_difference(cls, ticker, exchangeName, symbol, open, high, low, close, vol, dateTime):
        data = cls(ticker=ticker, exchangeName=exchangeName, symbol=symbol, open=open, high=high, low=low,
                   close=close, vol=vol, dateTime=dateTime)
        return data