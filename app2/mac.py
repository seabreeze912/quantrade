# -*- coding: utf-8 -*-
# mac.py

import datetime
import numpy as np
import pandas as pd
import os

from strategy import Strategy
from event import SignalEvent
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio


class MovingAverageCrossStrategy(Strategy):
    """
    基于MA来判断交易信号。
    """
    def __init__(self, bars, events, short_window=5, long_window=10):
        self.bars= bars
        self.events = events
        self.short_window = short_window
        self.long_window = long_window     
        self.symbol_list = bars.symbol_list
        
        self.bought = self._calculate_initial_bought()
       
        
    def _calculate_initial_bought(self):
        """
        初始化所有持仓列表，bought，所有股票状态为OUT
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] = "OUT"
        return bought
    
    
    def calculate_signals(self, event):
        """
        基于MA生成SignalEvent
        进入信号为短期MA超过长期MA
        """
        if event.type=="MARKET":
            for s in self.symbol_list:
                bar = self.bars.get_latest_bar(s)
                bars = self.bars.get_latest_bars_values(s, "adj_close", 
                                                        N=self.long_window)
                bar_date = self.bars.get_latest_bar_datetime(s)

                if bars.size >= self.long_window:
                    short_sma = np.mean(bars[-self.short_window: ])
                    long_sma = np.mean(bars[-self.long_window: ])

                    dt = datetime.datetime.utcnow()
                    sig_dir = ""
                    
                    # SMA > LMA，且当前持仓为空，没有停盘，开多单
                    if short_sma > long_sma and self.bought[s]=="OUT" and bar[1].isOpen == 1:
                        sig_dir = "LONG"
                        signal = SignalEvent(strategy_id=1,
                                             symbol=s, 
                                             datetime=dt,
                                             signal_type=sig_dir, 
                                             strength=1.0)                  
                        self.events.put(signal)
                        self.bought[s] = "LONG"
                    
                    # SMA < LMA，且当前持多仓，没有停盘，开空单
                    elif short_sma < long_sma and self.bought[s] == "LONG" and bar[1].isOpen == 1:
                        sig_dir='EXIT'
                        signal=SignalEvent(strategy_id=1,
                                           symbol=s, 
                                           datetime=dt,
                                           signal_type=sig_dir, 
                                           strength=1.0)                       
                        self.events.put(signal)
                        self.bought[s]='OUT'  
                        

if __name__ == "__main__":
    csv_dir = os.path.join(os.getcwd(), 'data\\HS300_dailydata_2015_2018.csv')
    
    symbol_df = pd.read_csv(csv_dir, usecols=['ticker'], dtype={'ticker':np.object})['ticker']
    day_num = pd.read_csv(csv_dir, usecols=['ticker'], dtype={'ticker':np.object})['ticker'].value_counts().max()
    symbol_list = list(symbol_df.value_counts()[(symbol_df.value_counts() >= day_num) == True].index)
    
    
    initial_capital = 500000.0
    heartbeat = 0
    start_date = datetime.datetime(2015,1,1,0,0,0)
     
    backtest = Backtest(csv_dir=csv_dir, 
                        symbol_list=symbol_list, 
                        initial_capital=initial_capital, 
                        heartbeat=heartbeat, 
                        start_date=start_date,
                        data_handler=HistoricCSVDataHandler, 
                        execution_handler=SimulatedExecutionHandler,
                        portfolio=Portfolio, 
                        strategy=MovingAverageCrossStrategy)
    
    curve, stats = backtest.simulate_trading()                  
                        

                        
