# -*- coding: utf-8 -*-
# jump_diffusion.py

import numpy as np

from .sn_random_numbers import sn_random_numbers
from .simulation_class import simulation_class


class jump_diffusion(simulation_class):
    """
    带跳跃的扩散过程模拟
    基于jump_diffusion模型
    """
    def __init__(self, name, mar_env, corr=False):
        super(jump_diffusion, self).__init__(name, mar_env, corr)
        
        try:
            self.lamb = mar_env.get_constant('lambda')
            self.mu = mar_env.get_constant('mu')
            self.delt = mar_env.get_constant('delta')
        except:
            print('市场环境参数输入错误！')
            
    
    def update(self, initial_value=None, volatility=None, final_date=None,
               lamb=None, mu=None, delt=None):
        if initial_value is not None:
            self.initial_value = initial_value
        
        if volatility is not None:
            self.volatility = volatility
            
        if final_date is not None:
            self.final_date = final_date
        
        if lamb is not None:
            self.lamb = lamb
        
        if mu is not None:
            self.mu = mu
        
        if delt is not None:
            self.delt = delt
            
        self.instrument_values = None
        
    
    def generate_paths(self, fixed_seed=False, day_count=365.):
         
        if self.time_grid is None:
            self.generate_time_grid()

        M = len(self.time_grid)
        I = self.paths
        paths = np.zeros((M, I))
        paths[0] = self.initial_value
 
        if not self.correlated:
            sn1 = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            sn1 = self.random_numbers
            
        sn2 = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        
        rj = self.lamb*(np.exp(self.mu + 0.5*self.delt**2) - 1)
        
        short_rate = self.discount_curve.short_rate
        
        for t in range(1, len(self.time_grid)):
            if not self.correlated:
                ran = sn1[t]
            else:
                ran = np.dot(self.cholesky_matrix, sn1[:, t, :])
                ran = ran[self.rn_set]
            
            dt = (self.time_grid[t] - self.time_grid[t-1]).days/day_count
            poi = np.random.poisson(self.lamb*dt, I)
            
            paths[t] = paths[t-1]*(np.exp((short_rate - rj -0.5*self.volatility**2)*dt + 
                 self.volatility*np.sqrt(dt)*ran) + (np.exp(self.mu + self.delt*sn2[t])-1)*poi)
            
        self.instrument_values = paths
        
"""
测试
   
from dx_frame import *      
me_jd = market_environment('me_jd', dt.datetime(2015,1,1))
me_jd.add_constant('lambda', 0.3)
me_jd.add_constant('mu', -0.75)
me_jd.add_constant('delta', 0.1)

me_jd.add_environment(me_gbm)

from jump_diffusion import jump_diffusion

jd = jump_diffusion('jd', me_jd)
path_3 = jd.get_instrument_values()


更新为高lambda,即高跳跃性

jd.update(lamb=0.9)
path_4 = jd.get_instrument_values()


作图

import matplotlib.pyplot as plt
% matplotlib inline

plt.figure(figsize=(8,4))
p1 = plt.plot(jd.time_grid, path_3[:,:10], 'b')
p2 = plt.plot(jd.time_grid, path_4[:,:10], 'r-.')
plt.grid(True)
l1 = plt.legend([p1[0], p2[0]], ['low_lambda', 'high_lambda'], loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.savefig('jd_test_01.jpg')
plt.show()

"""
        