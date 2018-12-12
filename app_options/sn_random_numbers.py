# -*- coding: utf-8 -*-
# sn_random_numbers.py

import numpy as np


def sn_random_numbers(shape, antithetic=True, moment_matching=True,
                      fixed_seed=False):
    
    if fixed_seed:
        np.random.seed(1000)
        
    if antithetic:
        """
        由符号相反的两部分随机数构成
        """
        ran = np.random.standard_normal((shape[0], shape[1], int(shape[2]/2)))
        ran = np.concatenate((ran, -ran), axis=2)
    else:
        ran = np.random.standard_normal(shape)
        
    if moment_matching:
        """
        标准化为01正态分布
        """
        ran = ran-np.mean(ran)
        ran = ran/np.std(ran)
        
    if shape[0]==1:
        return ran[0]
    else:
        return ran
    