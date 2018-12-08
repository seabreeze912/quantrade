from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import requests
import pandas as pd
import datetime

from .models import BtcDailyData, BtcDifference

# ******************主页******************
def home(request):
    return render(request, 'app1/home.html')


# *******************策略1 - 测试普通数据 ****************
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


# *****************策略2 - 测试动态图******************

def data_fresh(request):
    btc_daily_data_close = BtcDailyData.objects.values_list('close')
    btc_daily_data_close_list = []
    for item in btc_daily_data_close:
        btc_daily_data_close_list.append(item[0])

    btc_daily_data_date = BtcDailyData.objects.values_list('dateTime')
    btc_daily_data_date_list = []
    for item in btc_daily_data_date:
        btc_daily_data_date_list.append(item[0].strftime("%Y-%m-%d"))

    context = {"data1": btc_daily_data_close_list,
               "data2": btc_daily_data_date_list}

    return JsonResponse(context)


def strategy02(request):
    return render(request, 'app1/strategy02.html')


# ******************策略3 - 测试基差 **************

# ********获取数据***********

def get_btc_tick_data(ticker):
    url = 'http://api.coindog.com/api/v1/tick/' + ticker + '?unit=usd'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res = requests.get(url=url, headers=headers).json()
    data = BtcDifference.create_btc_difference(ticker=res['ticker'],
                                               exchangeName=res['exchangeName'],
                                               symbol=res['symbol'],
                                               open=res['open'],
                                               high=res['high'],
                                               low=res['low'],
                                               close=res['close'],
                                               vol=res['vol'],
                                               dateTime=float(res['dateTime']))

    if BtcDifference.objects.filter(ticker=res['ticker'], dateTime=res['dateTime']).count() == 0:
        data.save()


def comments_upload(request):
    if request.method == 'POST':
        print("it's a test")                            #用于测试
        print(request.POST['input'])           #测试是否能够接收到前端发来的input字段
        return HttpResponse('<span style="line-height: 1.42857;">'+ request.POST["input"] +'</span><span style="line-height: 1.42857;">')
    else:
        return HttpResponse("<h1>test</h1>")


def strategy03(request):
    get_btc_tick_data(ticker='HUOBIPRO:BTCUSDT')
    get_btc_tick_data(ticker='OKEX:BTCUSDT')




    return render(request, 'app1/strategy03.html')