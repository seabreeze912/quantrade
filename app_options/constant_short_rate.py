# -*- coding: utf-8 -*-

# constant_short_rate.py

from .get_year_deltas import *


class constant_short_rate(object):
    """
    该类用于短期利率的贴现
    """
    def __init__(self, name, short_rate):
        self.name = name
        self.short_rate = short_rate
        
        if short_rate<0:
            raise ValueError('短期利率不能为负！')
            
            
    def get_discount_factores(self, date_list, dtobjects=True):
        """
        dtobjects表示传入的date_list是否为datetime格式，默认为true
        """
        if dtobjects is True:
            dlist = get_year_deltas(date_list)
        else:
            dlist = np.array(date_list)
        
        dflist = np.exp(self.short_rate*np.sort(-dlist))
        
        return np.array((date_list, dflist)).T
        
    