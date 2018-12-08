# -*- coding: utf-8 -*-
# strategy.py

from abc import ABCMeta,abstractmethod
import datetime
import queue
import numpy as np
import pandas as pd

from event import SignalEvent

class Strategy(object):
    """
    Strategy类是一个抽象类，提供所有策略处理对象的接口。
    """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def caluclate_signals(self):
        """
        提供交易信号计算方式
        """
        raise NotImplementedError("Should implement calculate_signals()")        