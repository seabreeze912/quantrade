# -*- coding: utf-8 -*-
# performance.py
"""
用于评价业绩的情况
"""

import numpy as np
import pandas as pd


def create_sharpe_ratio(returns, periods=252):
    """
    计算策略的Sharpe比率，假设无风险利率为0
    """  
    return np.sqrt(periods)*(np.mean(returns)/np.std(returns))


def create_drawdowns(pnl):
    """
    计算最大回撤，以及回撤持续的时间
    这里参数pnl_returns为Series
    """
    hwm = [0]
    idx = pnl.index
    drawdown = pd.Series(index=idx)
    duration = pd.Series(index=idx)
    
    for t in range(1,len(idx)):
        hwm.append(max(hwm[t-1], pnl[t]))
        drawdown[t] = (hwm[t] - pnl[t])
        duration[t] = (0 if drawdown[t]==0 else duration[t-1]+1)
        
    return drawdown, drawdown.max(), duration.max()

    
    
        