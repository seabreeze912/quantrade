# -*- coding: utf-8 -*-
# execution.py

from abc import ABCMeta,abstractmethod
import datetime
import queue

from event import FillEvent,OrderEvent


class ExecutionHandler(object):
    """
    ExecutionHandler抽象类，处理由Portfolio生成的order。
    用于实际的成交，或者模拟的成交。
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def execute_order(self, event):
        """
        获取一个Order并执行，产生Fill事件
        """
        raise NotImplementedError("Should implement execute_order()")


class SimulatedExecutionHandler(ExecutionHandler):
    """
    模拟交易的执行处理，简单的将所有的订单转化为相同价格的的成交，不考虑
    时延，滑价以及成交比率的影响。
    """
    def __init__(self, events):
        self.events = events
        
    def execute_order(self, event):
        """
        简单的将订单转化为成交交易，不考虑时延、滑点及成交比率等的影响。
        """
        if event.type == "ORDER":
            fill_event = FillEvent(datetime.datetime.utcnow(),
                                   event.symbol,
                                   "Exchange",
                                   event.quantity,
                                   event.direction,
                                   None)
            self.events.put(fill_event)
        
        