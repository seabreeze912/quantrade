from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import matplotlib.pyplot as plt


# 衍生品分析库
import datetime as dt
from .get_year_deltas import get_year_deltas
from .constant_short_rate import constant_short_rate
from .market_environment import market_environment

from .geometric_brownian_motion import geometric_brownian_motion





def gbm(request):
    if request.method == 'POST':
        me_gbm = market_environment('me_gbm', dt.datetime(int(request.POST['pricing_date_y']), int(request.POST['pricing_date_m']), int(request.POST['pricing_date_d'])))
        me_gbm.add_constant('final_date', dt.datetime(int(request.POST['final_date_y']), int(request.POST['final_date_m']),int(request.POST['final_date_d'])))

        me_gbm.add_constant('initial_value', float(request.POST['initial_value']))
        me_gbm.add_constant('volatility', float(request.POST['volatility']))

        me_gbm.add_constant('frequency', str(request.POST['frequency']))
        me_gbm.add_constant('paths', int(request.POST['paths']))
        csr = constant_short_rate('csr', float(request.POST['csr']))
        me_gbm.add_curve('discount_curve', csr)

        me_gbm.add_constant('currency', str(request.POST['currency']))

        # 生成低波动情况下路径
        gbm = geometric_brownian_motion('gbm', me_gbm)
        path_1 = gbm.get_instrument_values()


        # 作图
        # plt.figure(figsize=(8, 4))
        # p1 = plt.plot(gbm.time_grid, path_1[:, :10], 'b')
        # p2 = plt.plot(gbm.time_grid, path_2[:, :10], 'r-.')
        # plt.grid(True)
        # l1 = plt.legend([p1[0], p2[0]], ['low_volatility', 'high_volatility'], loc=2)
        # plt.gca().add_artist(l1)
        # plt.xticks(rotation=30)
        # plt.savefig('gbm_test_01.jpg')
        # plt.show()

        data = list(path_1[-1])
        return render(request, 'app3/gbm.html', {'data': data})
    else:
        data = [1,2,3,4,5]
        return render(request, 'app3/gbm.html', {'data': data})
