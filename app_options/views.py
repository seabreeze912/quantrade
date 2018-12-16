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

from .valuation_class import valuation_class
from .geometric_brownian_motion import geometric_brownian_motion
from .valuation_mcs_european import valuation_mcs_european
from .valuation_mcs_american import valuation_mcs_american

# **********************************************************************************************************************
# home页
def home(request):
    return render(request, 'app_options/home.html', )


# 金融建模主页
def fin_mode_home(request):
    return render(request, 'app_options/fin_mode.html', )


# **********************************************************************************************************************
# gbm网站链接
def options_gbm(request):
    return render(request, 'app_options/options_gbm.html', )


# POST参数后，用于获取gbm模拟数据
@csrf_exempt
def gbm_json(request):
    if request.method == 'POST':
        option_model = str(request.POST['option_model'])

        # #####################
        # 欧式期权 #
        # #####################
        if option_model == 'European':
            data = {}
            # ************************直方图处理逻辑**********************************************************************
            # 设置gbm参数
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

            # 生成gbm模拟路径，随机种子为true
            gbm = geometric_brownian_motion('gbm', me_gbm)
            path = gbm.get_instrument_values(fixed_seed=False)

            data['instrument_values'] = list(path[-1])

            # ************************随机路径图处理逻辑******************************************************************
            # 保存所有模拟路径为df
            path_dataframe = pd.DataFrame(path, index=gbm.time_grid)

            # 保存时间序列
            time_list = list(path_dataframe.index.strftime('%Y-%m-%d'))
            data['time_list'] = time_list
            # 时间转换为数列的array，并合并为[[date, value], [date, value]...]的形式
            # time_grid = np.array(list(int(time.mktime(i.timetuple()) * 1000) for i in path_dataframe.index))
            # time_grid = time_grid.reshape(time_grid.shape[0], 1)

            # 随机获取100条路径，保存到dict中
            path_num = int(request.POST['paths'])
            random_path_index_list = list(np.random.randint(1, path_num, size=100))
            random_path = {}
            for i, val in enumerate(random_path_index_list):
                path = path_dataframe[val].values
                random_path[str(i)] = list(float('%4.2f' % i) for i in path)

            data['random_path'] = random_path

            # ************************欧式期权估值处理逻辑*****************************************************************
            # ！！！                                                                            ！！！
            # ！！！这里注意，之前已经计算了一次价值，所有时间区间不为空，maturity无法加入到其中。所以需要新建一个实例
            # ！！！                                                                            ！！！
            # ************************欧式看涨期权************************************************************************
            # 生成看涨期权估值环境
            me_gbm1 = market_environment('me_gbm', dt.datetime(int(request.POST['pricing_date_y']),
                                                              int(request.POST['pricing_date_m']),
                                                              int(request.POST['pricing_date_d'])))

            me_gbm1.add_constant('final_date', dt.datetime(int(request.POST['final_date_y']),
                                                          int(request.POST['final_date_m']),
                                                          int(request.POST['final_date_d'])))

            me_gbm1.add_constant('initial_value', float(request.POST['initial_value']))
            me_gbm1.add_constant('volatility', float(request.POST['volatility']))
            me_gbm1.add_constant('frequency', str(request.POST['frequency']))
            me_gbm1.add_constant('paths', int(request.POST['paths']))
            csr1 = constant_short_rate('csr', float(request.POST['csr']))
            me_gbm1.add_curve('discount_curve', csr1)

            me_gbm1.add_constant('currency', str(request.POST['currency']))

            # 生成gbm模拟路径，随机种子为true
            gbm1 = geometric_brownian_motion('gbm', me_gbm1)

            me_call = market_environment('me_call', me_gbm1.pricing_date)
            me_call.add_constant('maturity', dt.datetime(int(request.POST['maturity_date_y']),
                                                        int(request.POST['maturity_date_m']),
                                                        int(request.POST['maturity_date_d'])))
            me_call.add_constant('strike', float(request.POST['strike']))
            me_call.add_constant('currency', str(request.POST['option_currency']))

            # 欧式看涨期权价值
            call_payoff_func = 'np.maximum(maturity_value - strike, 0)'

            eur_call = valuation_mcs_european('eur_call', underlying=gbm1, mar_env=me_call,
                                              payoff_func=call_payoff_func)

            call_options_values_frame = eur_call.present_value(fixed_seed=False, full=True)
            call_all_options_values = list(call_options_values_frame[1])
            call_options_value = call_options_values_frame[0]

            data['call_all_options_values'] = call_all_options_values
            data['call_options_value'] = call_options_value

            # ************************欧式看涨期权希腊字母*****************************************************************
            s0 = float(request.POST['initial_value'])
            k0 = float(request.POST['strike'])
            min_s_k = min(s0, k0)
            max_s_k = max(s0, k0)
            s_list = list(np.arange(min_s_k/2, max_s_k*2, 0.5))
            # print(s_list)

            call_p_list = []
            call_d_list = []
            call_g_list = []
            call_v_list = []
            call_t_list = []
            call_r_list = []

            for s in s_list:
                eur_call.update(initial_value=s)
                call_p_list.append(eur_call.present_value(fixed_seed=True))
                call_d_list.append(eur_call.delta())
                call_g_list.append(eur_call.gamma())
                call_v_list.append(eur_call.vega())
                call_t_list.append(eur_call.theta())
                call_r_list.append(eur_call.rho())

            data['s_list'] = s_list
            data['call_p_list'] = call_p_list
            data['call_d_list'] = call_d_list
            data['call_v_list'] = call_v_list
            data['call_g_list'] = call_g_list
            data['call_t_list'] = call_t_list
            data['call_r_list'] = call_r_list

            # ************************欧式看跌期权************************************************************************

            gbm2 = geometric_brownian_motion('gbm', me_gbm1)
            put_payoff_func = 'np.maximum(strike - maturity_value, 0)'

            eur_put = valuation_mcs_european('eur_call', underlying=gbm2, mar_env=me_call,
                                             payoff_func=put_payoff_func)
            put_options_values_frame = eur_put.present_value(fixed_seed=False, full=True)
            put_all_options_values = list(put_options_values_frame[1])
            put_options_value = put_options_values_frame[0]

            data['put_all_options_values'] = put_all_options_values
            data['put_options_value'] = put_options_value

            # ************************欧式看跌期权希腊字母*****************************************************************
            put_p_list = []
            put_d_list = []
            put_g_list = []
            put_v_list = []
            put_t_list = []
            put_r_list = []

            for s in s_list:
                eur_put.update(initial_value=s)
                put_p_list.append(eur_put.present_value(fixed_seed=True))
                put_d_list.append(eur_put.delta())
                put_v_list.append(eur_put.vega())
                put_g_list.append(eur_put.gamma())
                put_t_list.append(eur_put.theta())
                put_r_list.append(eur_put.rho())

            data['put_p_list'] = put_p_list
            data['put_d_list'] = put_d_list
            data['put_v_list'] = put_v_list
            data['put_g_list'] = put_g_list
            data['put_t_list'] = put_t_list
            data['put_r_list'] = put_r_list

            return HttpResponse(json.dumps(data), content_type='application/json')

        # #####################
        # 美式期权 #
        # #####################
        else:
            data = {}
            # ************************直方图处理逻辑**********************************************************************
            # 设置gbm参数
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

            # 生成gbm模拟路径，随机种子为true
            gbm = geometric_brownian_motion('gbm', me_gbm)
            path = gbm.get_instrument_values(fixed_seed=False)

            data['instrument_values'] = list(path[-1])

            # ************************随机路径图处理逻辑******************************************************************
            # 保存所有模拟路径为df
            path_dataframe = pd.DataFrame(path, index=gbm.time_grid)

            # 保存时间序列
            time_list = list(path_dataframe.index.strftime('%Y-%m-%d'))
            data['time_list'] = time_list
            # 时间转换为数列的array，并合并为[[date, value], [date, value]...]的形式
            # time_grid = np.array(list(int(time.mktime(i.timetuple()) * 1000) for i in path_dataframe.index))
            # time_grid = time_grid.reshape(time_grid.shape[0], 1)

            # 随机获取100条路径，保存到dict中
            path_num = int(request.POST['paths'])
            random_path_index_list = list(np.random.randint(1, path_num, size=100))
            random_path = {}
            for i, val in enumerate(random_path_index_list):
                path = path_dataframe[val].values
                random_path[str(i)] = list(float('%4.2f' % i) for i in path)

            data['random_path'] = random_path

            # ************************美式期权估值处理逻辑*****************************************************************
            # ！！！                                                                            ！！！
            # ！！！这里注意，之前已经计算了一次价值，所有时间区间不为空，maturity无法加入到其中。所以需要新建一个实例
            # ！！！                                                                            ！！！
            # ************************欧式看涨期权************************************************************************
            # 生成看涨期权估值环境
            me_gbm1 = market_environment('me_gbm', dt.datetime(int(request.POST['pricing_date_y']),
                                                              int(request.POST['pricing_date_m']),
                                                              int(request.POST['pricing_date_d'])))

            me_gbm1.add_constant('final_date', dt.datetime(int(request.POST['final_date_y']),
                                                          int(request.POST['final_date_m']),
                                                          int(request.POST['final_date_d'])))

            me_gbm1.add_constant('initial_value', float(request.POST['initial_value']))
            me_gbm1.add_constant('volatility', float(request.POST['volatility']))
            me_gbm1.add_constant('frequency', str(request.POST['frequency']))
            me_gbm1.add_constant('paths', int(request.POST['paths']))
            csr1 = constant_short_rate('csr', float(request.POST['csr']))
            me_gbm1.add_curve('discount_curve', csr1)

            me_gbm1.add_constant('currency', str(request.POST['currency']))

            # 生成gbm模拟路径，随机种子为true
            gbm1 = geometric_brownian_motion('gbm', me_gbm1)

            me_call = market_environment('me_call', me_gbm1.pricing_date)
            me_call.add_constant('maturity', dt.datetime(int(request.POST['maturity_date_y']),
                                                        int(request.POST['maturity_date_m']),
                                                        int(request.POST['maturity_date_d'])))
            me_call.add_constant('strike', float(request.POST['strike']))
            me_call.add_constant('currency', str(request.POST['option_currency']))

            # 美式看涨期权价值
            call_payoff_func = 'np.maximum(instrument_values - strike, 0)'

            eur_call = valuation_mcs_american('eur_call', underlying=gbm1, mar_env=me_call,
                                              payoff_func=call_payoff_func)

            call_options_values_frame = eur_call.present_value(fixed_seed=False, full=True)
            call_all_options_values = list(call_options_values_frame[1])
            call_options_value = call_options_values_frame[0]

            data['call_all_options_values'] = call_all_options_values
            data['call_options_value'] = call_options_value

            # ************************期权希腊字母***********************************************************************

            s0 = float(request.POST['initial_value'])
            k0 = float(request.POST['strike'])
            min_s_k = min(s0, k0)
            max_s_k = max(s0, k0)
            s_list = list(np.arange(min_s_k/2, max_s_k*2, 0.5))
            # print(s_list)

            call_p_list = []
            call_d_list = []
            call_g_list = []
            call_v_list = []
            call_t_list = []
            call_r_list = []

            for s in s_list:
                eur_call.update(initial_value=s)
                call_p_list.append(eur_call.present_value(fixed_seed=True))
                call_d_list.append(eur_call.delta())
                call_g_list.append(eur_call.gamma())
                call_v_list.append(eur_call.vega())
                call_t_list.append(eur_call.theta())
                call_r_list.append(eur_call.rho())

            data['s_list'] = s_list
            data['call_p_list'] = call_p_list
            data['call_d_list'] = call_d_list
            data['call_v_list'] = call_v_list
            data['call_g_list'] = call_g_list
            data['call_t_list'] = call_t_list
            data['call_r_list'] = call_r_list

            # ************************欧式看跌期权************************************************************************

            gbm2 = geometric_brownian_motion('gbm', me_gbm1)
            put_payoff_func = 'np.maximum(strike - instrument_values, 0)'

            eur_put = valuation_mcs_american('eur_call', underlying=gbm2, mar_env=me_call,
                                             payoff_func=put_payoff_func)
            put_options_values_frame = eur_put.present_value(fixed_seed=False, full=True)
            put_all_options_values = list(put_options_values_frame[1])
            put_options_value = put_options_values_frame[0]

            data['put_all_options_values'] = put_all_options_values
            data['put_options_value'] = put_options_value

            # ************************欧式看跌期权希腊字母*****************************************************************
            put_p_list = []
            put_d_list = []
            put_g_list = []
            put_v_list = []
            put_t_list = []
            put_r_list = []

            for s in s_list:
                eur_put.update(initial_value=s)
                put_p_list.append(eur_put.present_value(fixed_seed=True))
                put_d_list.append(eur_put.delta())
                put_v_list.append(eur_put.vega())
                put_g_list.append(eur_put.gamma())
                put_t_list.append(eur_put.theta())
                put_r_list.append(eur_put.rho())

            data['put_p_list'] = put_p_list
            data['put_d_list'] = put_d_list
            data['put_v_list'] = put_v_list
            data['put_g_list'] = put_g_list
            data['put_t_list'] = put_t_list
            data['put_r_list'] = put_r_list

            return HttpResponse(json.dumps(data), content_type='application/json')

