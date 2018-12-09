# -*- coding: utf-8 -*-

# get_year_deltas.py

import numpy as np


def get_year_deltas(date_list, day_count=365.):
    """
    返回以年的比例表示的日期间隔列表
    """
    start = date_list[0]
    delta_list = [(date-start).days/day_count for date in date_list]
    
    return np.array(delta_list)