from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import matplotlib.pyplot as plt
import json
import random
import time
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)


# 衍生品分析库
import datetime as dt
from .get_year_deltas import get_year_deltas
from .constant_short_rate import constant_short_rate
from .market_environment import market_environment

from .geometric_brownian_motion import geometric_brownian_motion


# gbm网站链接
def gbm(request):
    return render(request, 'app3/gbm.html',)


# 设置全局变量
path_num = []
path_dataframe = []

# POST参数后，用于获取gbm模拟数据
@csrf_exempt
def gbm_json(request):
    global path_dataframe, path_num

    if request.method == 'POST':
        me_gbm = market_environment('me_gbm', dt.datetime(int(request.POST['pricing_date_y']),
                                                          int(request.POST['pricing_date_m']),
                                                          int(request.POST['pricing_date_d'])))
        me_gbm.add_constant('final_date', dt.datetime(int(request.POST['final_date_y']),
                                                      int(request.POST['final_date_m']),
                                                      int(request.POST['final_date_d'])))

        me_gbm.add_constant('initial_value', float(request.POST['initial_value']))
        me_gbm.add_constant('volatility', float(request.POST['volatility']))

        me_gbm.add_constant('frequency', str(request.POST['frequency']))
        me_gbm.add_constant('paths', int(request.POST['paths']))
        csr = constant_short_rate('csr', float(request.POST['csr']))
        me_gbm.add_curve('discount_curve', csr)

        me_gbm.add_constant('currency', str(request.POST['currency']))

        # 生成模拟路径，随机种子为true
        gbm = geometric_brownian_motion('gbm', me_gbm)
        path = gbm.get_instrument_values(fixed_seed=False)

        path_dataframe = pd.DataFrame(path, index=gbm.time_grid)
        path_num = int(request.POST['paths'])
        data = {'data': list(path[-1])}

    return HttpResponse(json.dumps(data), content_type='application/json')


def gbm_json_path_data(request):
    global path_dataframe, path_num

    # 时间转换为数列的array，并合并为[[date, value], [date, value]...]的形式
    time_grid = np.array(list(int(time.mktime(i.timetuple()) * 1000) for i in path_dataframe.index))
    time_grid = time_grid.reshape(time_grid.shape[0], 1)

    path_num_1 = random.randint(0, path_num)
    path = path_dataframe[path_num_1].values
    path = path.reshape(path.shape[0], 1)

    path_data = np.hstack((time_grid, path)).tolist()
    path_data = {'path_data': path_data}

    # 转换为一维列表形式
    time_list = list(path_dataframe.index.strftime('%Y-%m-%d'))

    path = path_dataframe[path_num_1].values
    path_list = list(float('%4.2f' % i )for i in path)

    path_data = {'time_list': time_list, 'path_list': path_list,}
    print(path_data)

    return HttpResponse(json.dumps(path_data), content_type='application/json')


def test01(request):
    return render(request, 'app_options/index.html', )

def test02(request):
    return render(request, 'app_options/options_gbm.html', )