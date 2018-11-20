from django.shortcuts import render

import requests
import pandas as pd
import datetime

from .models import BtcDailyData


def home(request):
    return render(request, 'app1/home.html')


def get_btc_daily_data():
    url = 'http://api.coindog.com/api/v1/klines/BITFINEX:BTCUSD/D1'
    res = requests.get(url).json()

    for item in res:
        data = BtcDailyData.create_btc_daily_data(item['close'],
                                                  datetime.datetime.fromtimestamp(float(item['dateTime'])/1000.0),
                                                  item['high'],
                                                  item['low'],
                                                  item['open'],
                                                  item['symbol'],
                                                  item['vol'],)
        try:
            data.save()
        except:
            print('数据已存在')
            continue


def strategy01(request):
    get_btc_daily_data()

    btc_daily_data = BtcDailyData.objects.all()
    print(btc_daily_data)

    return render(request, 'app1/strategy01.html', {'btc_daily_data': btc_daily_data})