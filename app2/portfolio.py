# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 18:20:34 2018

portfolio.py
"""

import datetime
from math import floor
import queue
import numpy as np
import pandas as pd

from event import FillEvent,OrderEvent
from performance import create_sharpe_ratio,create_drawdowns


class Portfolio(object):
    """
    Portfolio类，针对在每个时间点，计算所有的持仓头寸和价值
    postion DataFrame存放一个用时间做索引的【持仓数量】
    holdings DataFrame存放特定时间索引对应的每个代码的【现金】和总的市场【持仓价值】，
    以及资产组合总量的百分比变化。
    """    
    
    def __init__(self, bars, events, start_date, initial_capital=100000):
        self.bars = bars 
        self.events = events 
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital
        
        # 持有头寸
        self.all_positions = self.construct_all_positions() 
        self.current_positions = self.construct_current_positions()
  
        # 持有资产的市值
        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()
  
    
# ***************************初始化持仓头寸、市值******************************* 
    def construct_current_positions(self):
        """
        每一个回测日期的持仓头寸当日的情况
        """
        d = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        return d
    
    
    def construct_all_positions(self):  
        """
        以列表形式保存的，所有回测日的持仓头寸的总表
        """
        d = dict((k,v) for k,v in [(s,0.0) for s in self.symbol_list])
        d["datatime"] = self.start_date
        return [d]
    
    
    def construct_current_holdings(self):  
        """
        每一个回测日期的资产市值当日的情况
        """
        d = dict((k,v) for k,v in [(s, 0.0) for s in self.symbol_list])
        d["cash"] = self.initial_capital
        d["commission"] = 0.0
        d["total"] = self.initial_capital
        return d
        
    
    def construct_all_holdings(self):
        """
        以列表形式保存的，所有回测日的持仓的资产价值明细的总表
        """
        d = dict((k,v) for k,v in [(s, 0.0) for s in self.symbol_list])
        d["cash"] = self.initial_capital
        d["commission"] = 0.0
        d["total"] = self.initial_capital
        return [d]
         

# ***************************简化的生成订单*************************************
    def update_signal(self,event):
        """
        基于SignalEvent来生成订单
        返回OrderEvent
        """
        if event.type=='SIGNAL':
            order_event=self.generate_naive_order(event)
            self.events.put(order_event)
    
    
    def generate_naive_order(self,signal):
        """
        简单的生成一个订单，固定的数量，没有风险管理或头寸调整的考虑    
        """
        order=None
        
        symbol=signal.symbol
        direction=signal.signal_type
        strength=signal.strength
        
        mkt_quantity=100
        cur_quantity=self.current_positions[symbol]
        order_type='MKT'
        
        if direction=='LONG' and cur_quantity==0:
            order=OrderEvent(symbol,order_type,mkt_quantity,'BUY')
        if direction=='SHORT' and cur_quantity==0:
            order=OrderEvent(symbol,order_type,mkt_quantity,'SELL')
        if direction=='EXIT' and cur_quantity>0:
            order=OrderEvent(symbol,order_type,abs(cur_quantity),'SELL')
        if direction=='EXIT' and cur_quantity<0:
            order=OrderEvent(symbol,order_type,abs(cur_quantity),'BUY')
        
        return order


# ***************************订单成交后的处理*********************************** 
    def update_fill(self, event):
        """
        在接收到FillEvent之后，更新当前持仓头寸和市值
        """
        if event.type=='FILL':
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)
        
        
    def update_positions_from_fill(self,fill):
        """
        更新持仓头寸
        """
        fill_dir=0
        if fill.direction=='BUY':
            fill_dir=1
        if fill.direction=='SELL':
            fill_dir=-1
        self.current_positions[fill.symbol] += fill_dir*fill.quantity
    
    
    def update_holdings_from_fill(self,fill):
        """
        更新持仓市值
        """
        fill_dir=0
        if fill.direction=='BUY':
            fill_dir=1
        if fill.direction=='SELL':
            fill_dir=-1
        
        fill_cost=self.bars.get_latest_bar_value(fill.symbol,"adj_close")
        cost=fill_dir * fill_cost * fill.quantity;
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)


    def update_timeindex(self,event):
        """
        根据最新行情，更新资产价值
        """
        latest_datatime = self.bars.get_latest_bar_datetime(self.symbol_list[0])
        
        # 更新当前持仓头寸，并添加到总表中
        dp = dict((k,v) for k,v in[(s,0) for s in self.symbol_list])
        dp["datetime"] = latest_datatime
        
        for s in self.symbol_list:
            dp[s] = self.current_positions[s]
            
        self.all_positions.append(dp)
        
        # 更新当前资产市值，并添加到总表中
        dh = dict((k,v) for k,v in [(s,0) for s in self.symbol_list])
        dh["datetime"] = latest_datatime
        dh["cash"] = self.current_holdings["cash"]
        dh["commission"] = self.current_holdings["commission"]
        dh["total"] = self.current_holdings["cash"]
        
        for s in self.symbol_list:
            market_value = self.current_positions[s]*self.bars.get_latest_bar_value(s, "adj_close")
            dh[s] = market_value
            dh["total"] += market_value
        
        self.all_holdings.append(dh)
        


# ***************************生成收益曲线，保存到csv*********************************** 
    def create_equity_curve_dataframe(self):        
        """
        基于all_holdings创建收益情况的DataFrame
        """
        curve = pd.DataFrame(self.all_holdings)     
        curve.set_index("datetime", inplace=True)
        curve["returns"] = curve["total"].pct_change()
        curve["equity_curve"] = (1.0 + curve["returns"]).cumprod()
        
        self.equity_curve = curve
        return curve
    
    def output_summary_stats(self):
        """
        保存资产组合的统计信息
        """
        total_return = self.equity_curve['equity_curve'][-1]
        returns = self.equity_curve['returns']
        pnl = self.equity_curve['equity_curve']
        
        sharpe_ratio = create_sharpe_ratio(returns)
        drawdown, max_dd, dd_duration = create_drawdowns(pnl)
        self.equity_curve['drawdown'] = drawdown
        
        stats=[("总收益为： ","%0.2f%%" % ((total_return-1.0)*100.0)),
               ("夏普比率为： ","%0.2f" % sharpe_ratio),
               ("最大回撤为： ","%0.2f%%" % (max_dd*100)),
               ("回撤时长为： ","%d" % dd_duration)]
        print(stats)
        
        self.equity_curve.to_csv('equity.csv')
        
        return stats








        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    