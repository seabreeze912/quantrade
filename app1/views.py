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

    btc_daily_data_close = BtcDailyData.objects.values_list('close')
    btc_daily_data_close_list = []
    for item in btc_daily_data_close:
        btc_daily_data_close_list.append(item[0])

    btc_daily_data_date = BtcDailyData.objects.values_list('dateTime')
    btc_daily_data_date_list = []
    for item in btc_daily_data_date:
        btc_daily_data_date_list.append(item[0].strftime("%Y-%m-%d"))

    return render(request, 'app1/strategy01.html', {'btc_daily_data': btc_daily_data,
                                                    'btc_daily_data_close_list': btc_daily_data_close_list,
                                                    'btc_daily_data_date_list': btc_daily_data_date_list,
                                                    })