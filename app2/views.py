from django.shortcuts import render

# Create your views here.
import os
import datetime
import pandas as pd

from .strategy import Strategy
from .event import SignalEvent
from .backtest import Backtest
from .data import HistoricCSVDataHandler
from .execution import SimulatedExecutionHandler
from .portfolio import Portfolio
from .mac import MovingAverageCrossStrategy

def


    csv_dir = os.path.join(os.getcwd(), 'data\\HS300_dailydata_2015_2018.csv')

    symbol_df = pd.read_csv(csv_dir, usecols=['ticker'], dtype={'ticker': np.object})['ticker']
    day_num = pd.read_csv(csv_dir, usecols=['ticker'], dtype={'ticker': np.object})['ticker'].value_counts().max()
    symbol_list = list(symbol_df.value_counts()[(symbol_df.value_counts() >= day_num) == True].index)

    initial_capital = 500000.0
    heartbeat = 0
    start_date = datetime.datetime(2015, 1, 1, 0, 0, 0)

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