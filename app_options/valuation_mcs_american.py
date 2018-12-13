# -*- coding: utf-8 -*-

# valuation_mcs_american.py

import numpy as np

from .valuation_class import valuation_class


class valuation_mcs_american(valuation_class):
    """
    单一因素模拟美式期权
    """
    def generate_payoff(self, fixed_seed=False):
        try:
            strike = self.strike
        except:
            pass
        
        paths = self.underlying.get_instrument_values(fixed_seed=fixed_seed)
        time_grid = self.underlying.time_grid
        
        try:
            time_index_start = int(np.where(time_grid==self.pricing_date)[0])
            time_index_end = int(np.where(time_grid==self.maturity)[0])
        except:
            print('到期日不在底层资产时间区间内！')
            
        instrument_values = paths[time_index_start : time_index_end+1]
        
        try:
            payoff = eval(self.payoff_func)
            return instrument_values, payoff, time_index_start, time_index_end
        except:
            print('Payoff func 异常！')
            
    
    def present_value(self, accuracy=6, fixed_seed=False, bf=5, full=False):
        # inner_values即payoff，为执行期权时的价格
        instrument_values, inner_values, time_index_start, time_index_end = self.generate_payoff(fixed_seed=fixed_seed)
        
        time_list = self.underlying.time_grid[time_index_start: time_index_end+1]
        discount_factor = self.discount_curve.get_discount_factores(time_list, dtobjects=True)
        
        V = inner_values[-1]
        for t in range(len(time_list)-2, 0, -1):
            df = discount_factor[t, 1] / discount_factor[t+1, 1]
            rg = np.polyfit(instrument_values[t], V*df, bf)
            C = np.polyval(rg, instrument_values[t])
            V  = np.where(inner_values[t] > C, inner_values[t], V*df)
            
        df = discount_factor[0, 1] / discount_factor[1, 1]
        result = np.sum(df*V) / len(V)
        
        if full:
            return round(result, accuracy), df*V
        else:
            return round(result, accuracy)        


'''

from dx import *

me_gbm = market_environment('me_gbm', dt.datetime(2015,1,1))
me_gbm.add_constant('initial_value', 36.0)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2016,12,31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'W')
me_gbm.add_constant('paths', 5000)

csr = constant_short_rate('csr', 0.06)
me_gbm.add_curve('discount_curve', csr)
        
gbm = geometric_brownian_motion('gbm', me_gbm)

payoff_func = 'np.maximum(strike - instrument_values, 0)'
 
me_am_put = market_environment('me_am_put', dt.datetime(2015,1,1))
me_am_put.add_constant('maturity', dt.datetime(2015,12,31))
me_am_put.add_constant('strike', 40.0)
me_am_put.add_constant('currency', 'EUR')   

from valuation_mcs_american import valuation_mcs_american
 
am_put = valuation_mcs_american('am_put', underlying=gbm,  mar_env=me_am_put, 
                                payoff_func=payoff_func)

am_put.present_value(fixed_seed=True, bf=5)


4.47248

%%time
ls_table = []
for initial_value in (36., 38., 40., 42, 44.):
    for volatility in (0.2, 0.4):
        for maturity in (dt.datetime(2015,12,31), dt.datetime(2016,12,31)):
            am_put.update(initial_value=initial_value, volatility=volatility, maturity=maturity)
            ls_table.append([initial_value, volatility, maturity, am_put.present_value(fixed_seed=True, bf=5)])


%%time
s_list = np.arange(10., 100.1, 5)
p_list = []
d_list = []
v_list = []

for s in s_list:
    am_put.update(initial_value=s)
    p_list.append(am_put.present_value(fixed_seed=True))
    d_list.append(am_put.delta())
    v_list.append(am_put.vega())

from plot_option_stats import plot_option_stats
plot_option_stats(s_list, p_list, d_list, v_list)

'''
            
            
            
            
            
            
            
            
            
            

            
