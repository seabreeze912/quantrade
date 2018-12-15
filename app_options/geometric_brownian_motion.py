# -*- coding: utf-8 -*-

# geometric_brownian_motion.py

import numpy as np

from .sn_random_numbers import sn_random_numbers
from .simulation_class import simulation_class


class geometric_brownian_motion(simulation_class):
    """
    几何布朗运动模拟
    基于BSM模型
    """
    def __init__(self, name, mar_env, corr=False):
        super(geometric_brownian_motion, self).__init__(name, mar_env, corr)
               
    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        
        if volatility is not None:
            self.volatility = volatility
            
        if final_date is not None:
            self.final_date = final_date
            
        self.instrument_values = None

    def generate_paths(self, fixed_seed=True, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()
        
        M = len(self.time_grid)
        I = self.paths
        paths = np.zeros((M, I))
        paths[0] = self.initial_value
        
        if not self.correlated:
            rand = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            rand = self.random_numbers
            
        short_rate = self.discount_curve.short_rate
        
        for t in range(1, len(self.time_grid)):
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
            
            dt = (self.time_grid[t] - self.time_grid[t-1]).days/day_count
            paths[t] = paths[t-1]*np.exp(
                    (short_rate - 0.5*self.volatility**2)*dt +
                    self.volatility*np.sqrt(dt)*ran)
        
        self.instrument_values = paths
        

"""
测试

from dx_frame import *

me_gbm = market_environment('me_gbm', dt.datetime(2015,1,1))
me_gbm.add_constant('initial_value', 36.0)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2015,12,31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'M')
me_gbm.add_constant('paths', 10000)

csr = constant_short_rate('csr', 0.05)
me_gbm.add_curve('discount_curve', csr)


生成低波动情况下路径

gbm = geometric_brownian_motion('gbm', me_gbm)
path_1 = gbm.get_instrument_values()


更新为高波动率

gbm.update(volatility=0.5)
path_2 = gbm.get_instrument_values()


作图

import matplotlib.pyplot as plt
% matplotlib inline

plt.figure(figsize=(8,4))
p1 = plt.plot(gbm.time_grid, path_1[:,:10], 'b')
p2 = plt.plot(gbm.time_grid, path_2[:,:10], 'r-.')
plt.grid(True)
l1 = plt.legend([p1[0], p2[0]], ['low_volatility', 'high_volatility'], loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.savefig('gbm_test_01.jpg')
plt.show()


"""








