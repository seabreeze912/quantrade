# -*- coding: utf-8 -*-

# sqare_root_diffusion.py

import numpy as np

from .sn_random_numbers import sn_random_numbers
from .simulation_class import simulation_class


class sqare_root_diffusion(simulation_class):
    """
    平方根扩散过程模拟
    """
    def __init__(self, name, mar_env, corr=False):
        super(sqare_root_diffusion,self).__init__(name, mar_env, corr)
        
        try:
            self.kappa = mar_env.get_constant('kappa')
            self.theta = mar_env.get_constant('theta')
        except:
            print(name + ' sqare_root_diffusion环境参数输入错误！')
    
    def update(self, initial_value=None, volatility=None, final_date=None,
               kappa=None, theta=None):
        if initial_value is not None:
            self.initial_value = initial_value
        
        if volatility is not None:
            self.volatility = volatility
            
        if final_date is not None:
            self.final_date = final_date
        
        if kappa is not None:
            self.kappa = kappa
        
        if theta is not None:
            self.theta = theta
            
        self.instrument_values = None    
    
    
    def generate_paths(self, fixed_seed=False, day_count=365.):
         
        if self.time_grid is None:
            self.generate_time_grid()

        M = len(self.time_grid)
        I = self.paths
        
        paths = np.zeros((M, I))
        paths_= np.zeros_like(paths) 
        paths[0] = self.initial_value
        paths_[0] = self.initial_value
        
        if not self.correlated:
            rand = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            rand = self.random_numbers
            
        for t in range(1, len(self.time_grid)):
            dt = (self.time_grid[t] - self.time_grid[t-1]).days/day_count
            
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
                
            paths_[t] = (paths_[t-1] + 
                  self.kappa*(self.theta - np.maximum(0, paths_[t-1,:]))*dt +
                  np.sqrt(np.maximum(0, paths_[t-1, :]))*self.volatility*np.sqrt(dt)*ran)
            
            paths[t] = np.maximum(0, paths_[t])
            
        self.instrument_values = paths

'''
from dx_frame import *

me_srd = market_environment('me_srd', dt.datetime(2015,1,1))
me_srd.add_constant('initial_value', 0.25)
me_srd.add_constant('volatility', 0.05)
me_srd.add_constant('final_date', dt.datetime(2015,12,31))
me_srd.add_constant('currency', 'EUR')
me_srd.add_constant('frequency', 'W')
me_srd.add_constant('paths', 10000)

me_srd.add_constant('kappa', 4.0)
me_srd.add_constant('theta', 0.2)

csr = constant_short_rate('csr', 0.0)
me_srd.add_curve('discount_curve', csr)

from sqare_root_diffusion import sqare_root_diffusion

srd = sqare_root_diffusion('srd', me_srd)

path_5 = srd.get_instrument_values()

srd.update(initial_value=0.15)
path_6 = srd.get_instrument_values()

import matplotlib.pyplot as plt
% matplotlib inline

plt.figure(figsize=(8,4))

p1 = plt.plot(srd.time_grid, path_5[:,:10], 'b')
p2 = plt.plot(srd.time_grid, path_6[:,:10], 'r-.')

plt.axhline(me_srd.get_constant('theta'), color='g', ls='--', lw=2.0)

plt.grid(True)
l1 = plt.legend([p1[0], p2[0]], ['high_initial_value', 'low_initial_value'], loc=4)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.savefig('srd_test_01.jpg')
plt.show()

'''





