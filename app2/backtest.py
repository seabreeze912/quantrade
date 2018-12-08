# -*- coding: utf-8 -*-
# backtest.py


import datetime
import pprint
import queue
import time


class Backtest(object):
    """
    事件驱动回测的组成，包括： 数据处理类，策略类，订单执行类， 资产管理类
    """
    def __init__(self, csv_dir, symbol_list, initial_capital, heartbeat,
                 start_date, data_handler, execution_handler, portfolio,
                 strategy):
        
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.initial_capital = initial_capital
        self.heartbeat =heartbeat
        self.start_date = start_date
        
        self.data_handler_cls = data_handler
        self.execution_handler_cls = execution_handler
        self.portfolio_cls = portfolio
        self.strategy_cls = strategy
        
        self.events = queue.Queue()
        
        self.signals = 0
        self.orders = 0
        self.fills = 0
        
        self._generate_trading_instances()
        
    def _generate_trading_instances(self):
        """
        将各个类实例化
        """
        print("创建数据处理类，策略类，订单执行类，资产管理类实例...")
        
        # 数据处理类
        self.data_handler = self.data_handler_cls(self.events, 
                                                  self.csv_dir,
                                                  self.symbol_list)
        
        # 策略类
        self.strategy = self.strategy_cls(self.data_handler,
                                          self.events)
        
        # 交易执行类
        self.execution_handler = self.execution_handler_cls(self.events)
 
        # 资产管理类
        self.portfolio = self.portfolio_cls(self.data_handler,
                                            self.events,
                                            self.start_date,
                                            self.initial_capital)
        
            
# ******************************回测程序***************************************        
    def _run_backtest(self):
        """
        回测程序          
        """      
        i = 0
        while True:
            i += 1
            # print(i)
            if self.data_handler.continue_backtest==True:
                self.data_handler.update_bars()
            else:
                # 所有数据取完后退出
                break
                
            while True:
                try:
                    event=self.events.get(block=False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == "MARKET":
                            '''
                            根据获取的行情计算交易信号，并更新持仓价值，
                            生成生成SignalEvent
                            '''
                            self.strategy.calculate_signals(event)
                            self.portfolio.update_timeindex(event)
                                                      
                        elif event.type=='SIGNAL':
                            '''
                            根据交易信号，生成交易订单，
                            如果出现买卖信号，生成OrderEvent
                            '''
                            self.signals+=1
                            self.portfolio.update_signal(event)
                         
                        elif event.type == "ORDER":
                            """
                            执行定单，生成成交情况，即FillEvent                           
                            """
                            self.orders+=1
                            self.execution_handler.execute_order(event)   
                                                    
                        elif event.type=='FILL':
                            """
                            根据成交情况，更新持仓，循环结束
                            """
                            self.fills+=1
                            self.portfolio.update_fill(event)     

            time.sleep(self.heartbeat)  
        
        
    def _output_performance(self):
        """
        输出收益统计
        """      
        curve = self.portfolio.create_equity_curve_dataframe()
        print(self.portfolio.equity_curve.iloc[-1])
        
        print("统计策略收益情况...")
        stats=self.portfolio.output_summary_stats()

        print("出现交易信号次数为： %s" % self.signals)
        print("下订单次数为： %s" % self.orders)
        print("订单成交次数为： %s" % self.fills)
        
        return curve, stats


    def simulate_trading(self):      
        """
        回测，输出业绩
        """
        self._run_backtest()
        curve, stats = self._output_performance()
        return curve, stats
            

            
            

          