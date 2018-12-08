# -*- coding: utf-8 -*-
#data.py

from abc import ABCMeta,abstractmethod
import datetime
import os,os.path

import numpy as np
import pandas as pd
pd.set_option('display.max_columns',None)

from event import MarketEvent


class DataHandler(object):
    """
    DataHandler为抽象基类,提供所有后续的数据处理类的接口
    输出一组针对每个请求的代码的数据条（OHLCVI）
    模拟实际的交易策略并发送市场信号
    """
    __metaclass__=ABCMeta
    
    @abstractmethod
    def get_latest_bar(self,symbol):
        """
        返回最近的1条数据
        """
        raise NotImplementedError("Should implement get_latest_bar()")
    
    @abstractmethod
    def get_latest_bars(self,symbol,N=1):
        """
        返回最近的N条数据
        """
        raise NotImplementedError("Should implement get_latest_bars()")
    
    @abstractmethod
    def get_latest_bar_datetime(self,symbol):
        """
        返回最近数据对应的datetime
        """
        raise NotImplementedError("Should implement get_latest_bar_datetime()")
    
    @abstractmethod
    def get_latest_bar_value(self,symbol,val_type):
        """
        返回最近的数据中的OHLCV数据
        """
        raise NotImplementedError("Should implement get_latest_bar_value()")
    
    @abstractmethod
    def get_latest_bars_values(self,symbol,val_type,N=1):
        """
        返回最近的N条数据中OHLCV数据，如果没有那么多数据
        返回N-k条
        """
        raise NotImplementedError("Should implement get_latest_bars_values()")
    
    @abstractmethod
    def update_bars(self):
        """
        获取当前最新交易数据，可以模拟从实时行情接收数据
        """
        raise NotImplementedError("Should implement update_bars()")
    
    
# *****************************************************************************
class HistoricCSVDataHandler(DataHandler):
    """
    HistoricCSVDataHandler类用来读取CSV文件，并以此模拟真实交易情况。
    """
    def __init__(self, events, csv_dir, symbol_list):
        self.events=events
        self.csv_dir=csv_dir
        self.symbol_list=symbol_list
        
        self.symbol_data={}
        self.latest_symbol_data={}
        self.continue_backtest=True
        self.bar_index=0
        
        self._open_convert_csv_files()
    
    def _open_convert_csv_files(self):
        """
        从数据路径中打开CSV文件，将它们转化为pandas的DataFrame。
        这里假设数据来自于yahoo。
        """
        df = pd.read_csv(self.csv_dir, 
                         usecols=['ticker', 'tradeDate', 'openPrice', 'highestPrice', 
                                  'lowestPrice', 'closePrice', 'chgPct', 'isOpen',
                                  'accumAdjFactor'],
                         dtype={'ticker':np.object})
        
        df['adj_close'] = df['closePrice'] * df['accumAdjFactor']
        df['tradeDate'] = df['tradeDate'].apply(lambda x : x.replace('-',''))
        df = df.set_index('tradeDate')
        
        
        for s in self.symbol_list:
            self.symbol_data[s]=df[df['ticker'] == s].sort_index()
            self.symbol_data[s]=self.symbol_data[s].iterrows()
            
            self.latest_symbol_data[s]=[]
            

        
    def _get_new_bar(self, symbol):
        """
        使用股票生成器生成一条行情数据
        """
        for b in self.symbol_data[symbol]:
            yield b
    
    
    def update_bars(self):
        """
        模拟接收到市场行情,向队列中传入MarketEvent
        """
        for s in self.symbol_list:
            try:
                bar=next(self._get_new_bar(s))
            except StopIteration:
                self.continue_backtest=False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())
        
        
    def get_latest_bar(self,symbol):
        """
        从latest_symbol_data中返回最新1条数据条目
        """
        try:
            bars_list=self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data")
            raise
        else:
            return bars_list[-1]
    
    
    def get_latest_bars(self,symbol,N=1):
        """
        从latest_symbol_data中获取N条数据，如果没有那么多，则返回所有的数据
        """
        try:
            bars_list=self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data")
            raise
        else:
            return bars_list[-N:]
    
    
    def get_latest_bar_datetime(self,symbol):
        """
        返回最近的数据对应的datetime
        """
        try:
            bars_list=self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data")
            raise
        else:
            return bars_list[-1][0]
    
    
    def get_latest_bar_value(self,symbol,val_type):
        """
        返回最新1条行情的行情数据
        """
        try:
            bars_list=self.latest_symbol_data[symbol]
        except KeyError:
            print("That Symbol is not available in the historical data")
            raise
        else:
            return getattr(bars_list[-1][1],val_type)
    
    
    def get_latest_bars_values(self,symbol,val_type,N=1):
        """
        返回最近N条行情的行情数据
        """
        try:
            bars_list=self.get_latest_bars(symbol,N)
        except KeyError:
            print("That Symbol is not available in the historical data")
            raise
        else:
            return np.array([getattr(b[1],val_type) for b in bars_list])
    

            

