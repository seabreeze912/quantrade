# -*- coding: utf-8 -*-
# valuation_mcs_european.py

import numpy as np

from .valuation_class import valuation_class


class valuation_mcs_european(valuation_class):
    """
    对任意支付的欧式期权定价
    """
    def __init__(self, name, underlying, mar_env, payoff_func):
        super(valuation_mcs_european, self).__init__(name, underlying, mar_env, payoff_func)

    def generate_payoff(self, fixed_seed=False):
        try:
            strike = self.strike
        except:
            pass
        
        paths = self.underlying.get_instrument_values(fixed_seed=fixed_seed)
        time_grid = self.underlying.time_grid
        
        try:
            time_index = np.where(time_grid==self.maturity)[0]
            time_index = int(time_index)
        except:
            print('衍生品到期日不在底层资产时间区间中！')
        
        maturity_value = paths[time_index]
        
        # 到期日前所有的均值，用于计算奇异期权的价值
        mean_value = np.mean(paths[:time_index], axis=1)
        max_value = np.amax(paths[:time_index], axis=1)[-1]
        min_value = np.amin(paths[:time_index], axis=1)[-1]
        
        try:
            payoff = eval(self.payoff_func)
            return payoff
        except:
            print('Payoff func 异常！')
            
    
    def present_value(self, accuracy=6, fixed_seed=False, full=False):
        cash_flow = self.generate_payoff(fixed_seed=fixed_seed)
        discount_factor = self.discount_curve.get_discount_factores((self.pricing_date, self.maturity))[0,1]
        
        result = discount_factor*np.sum(cash_flow)/len(cash_flow)
        
        if full:
            return round(result, accuracy), discount_factor*cash_flow
        else:
            return round(result, accuracy)
        
'''
from dx import *

me_gbm = market_environment('me_gbm', dt.datetime(2015,1,1))
me_gbm.add_constant('initial_value', 36.0)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2015,12,31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'M')
me_gbm.add_constant('paths', 10000)

csr = constant_short_rate('csr', 0.06)
me_gbm.add_curve('discount_curve', csr)

gbm = geometric_brownian_motion('gbm', me_gbm)

me_call = market_environment('me_call', me_gbm.pricing_date)

me_call.add_constant('strike', 40.0)
me_call.add_constant('maturity', dt.datetime(2015,12,31))
me_call.add_constant('currency', 'EUR')


普通欧式期权
payoff_func = 'np.maximum(maturity_value - strike, 0)'

from valuation_mcs_european import valuation_mcs_european

eur_call = valuation_mcs_european('eur_call', underlying=gbm, 
                                  mar_env=me_call, payoff_func=payoff_func)

求解希腊字母
s_list = np.arange(30., 50.1, 0.2)
p_list = []
d_list = []
v_list = []

for s in s_list:
    eur_call.update(initial_value=s)
    p_list.append(eur_call.present_value(fixed_seed=True))
    d_list.append(eur_call.delta())
    v_list.append(eur_call.vega())


亚式期权
payoff_func = 'np.maximum(0.33*(maturity_value*max_value) - 40, 0)'
eur_as_call = valuation_mcs_european('eur_as_call', underlying=gbm, 
                                  mar_env=me_call, payoff_func=payoff_func)


s_list = np.arange(10., 100.1, 2)
p_list = []
d_list = []
v_list = []

for s in s_list:
    eur_as_call.update(initial_value=s)
    p_list.append(eur_as_call.present_value(fixed_seed=True))
    d_list.append(eur_as_call.delta())
    v_list.append(eur_as_call.vega())

from plot_option_stats import plot_option_stats
plot_option_stats(s_list, p_list, d_list, v_list)

'''