# -*- coding: utf-8 -*-

# valuation_class.py
import datetime
from .constant_short_rate import constant_short_rate


class valuation_class(object):
    """
    单一因素的估值基类
    """
    def __init__(self, name, underlying, mar_env, payoff_func):
        try:
            self.name = name
            self.pricing_date = mar_env.pricing_date
            
            try:
                self.strike = mar_env.get_constant('strike')
            except:
                pass
            
            self.maturity = mar_env.get_constant('maturity')
            
            self.currency = mar_env.get_constant('currency')
            
            self.frequency = underlying.frequency
            self.paths = underlying.paths           
            self.discount_curve = underlying.discount_curve
            
            self.payoff_func = payoff_func
            self.underlying = underlying
            self.underlying.special_dates.extend([self.pricing_date, self.maturity])
            # print('valuation_class + underlying.special_dates', self.underlying.special_dates)
            
        except:
            print(name + '衍生品估值的市场环境参数输入错误！')   

    def update(self, initial_value=None, volatility=None, strike=None,
               maturity=None, pricing_date=None, csr=None):
        '''
        注意: 此处修改的initial_value，volatility为底层资产的环境属性，所以需要用
        underlying.update来处理，而不是如strike或者maturity的形式。
        '''

        if initial_value is not None:
            self.underlying.update(initial_value=initial_value)
        
        if volatility is not None:
            self.underlying.update(volatility=volatility)
            
        if strike is not None:
            self.strike = strike
            
        if maturity is not None:
            self.maturity = maturity
            print('valuation_class + update', 1)
            if not maturity in self.underlying.time_grid:
                self.underlying.special_dates.append(maturity)
                print('valuation_class + update', self.underlying.special_dates)

        if pricing_date is not None:
            self.underlying.pricing_date = pricing_date
            self.pricing_date = pricing_date

            self.underlying.time_grid = None
            self.underlying.special_dates = []
            self.underlying.special_dates.extend([self.pricing_date, self.maturity])

        if csr is not None:
            self.underlying.discount_curve = None
            csr = constant_short_rate('csr', csr)
            self.underlying.discount_curve = csr
            self.discount_curve = self.underlying.discount_curve
                
        self.underlying.instrument_values = None

    def delta(self, interval=None, accuracy=4):
        if interval is None:
            interval = self.underlying.initial_value/50.
        
        value_left = self.present_value(fixed_seed=True)
        
        initial_del = self.underlying.initial_value + interval     
        self.underlying.update(initial_value=initial_del)
        
        value_right = self.present_value(fixed_seed=True)
        
        self.underlying.update(initial_value=initial_del - interval)
        
        delta = (value_right - value_left)/interval
        
        if delta<-1.0:
            return -1.0
        elif delta>1.0:
            return 1.0
        else:
            return round(delta, accuracy)

    def gamma(self, interval=None, accuracy=4):
        if interval is None:
            interval = self.underlying.initial_value / 10.

        # 期权原始价格
        value_origin = self.present_value(fixed_seed=True)

        # 计算初始价格 +0.5 个变动单位时的delta
        initial_del_right = self.underlying.initial_value + interval
        self.underlying.update(initial_value=initial_del_right)
        value_right = self.present_value(fixed_seed=True)
        delta_right = (value_right - value_origin) / interval

        # 计算初始价格 -0.5 个变动单位时的delta
        initial_del_left = initial_del_right - interval * 2
        self.underlying.update(initial_value=initial_del_left)
        value_left = self.present_value(fixed_seed=True)
        delta_left = (value_origin - value_left) / interval

        # 计算gamma
        gamma = (delta_right - delta_left) / interval / 2.0

        self.underlying.update(initial_value=initial_del_left + interval)
        return round(gamma, accuracy)

    def vega(self, interval=0.01, accuracy=4):
        if interval<self.underlying.volatility/20.0:
            interval = self.underlying.volatility/20.
        
        value_left = self.present_value(fixed_seed=True)
        
        vola_del = self.underlying.volatility + interval
        self.underlying.update(volatility=vola_del)
        
        value_right = self.present_value(fixed_seed=True)
        
        self.underlying.update(volatility=vola_del - interval)
        
        vega = (value_right - value_left)/interval
        
        return round(vega, accuracy)

    def theta(self, accuracy=4):
            value_origin = self.present_value(fixed_seed=True)

            pricing_date_origin = self.pricing_date
            new_pricing_date = pricing_date_origin + datetime.timedelta(days=1)
            self.update(pricing_date=new_pricing_date)
            value_new = self.present_value(fixed_seed=True)
            theta = value_new - value_origin

            self.update(pricing_date=pricing_date_origin)

            return round(theta, accuracy)

    def rho(self, accuracy=4):
        value_origin = self.present_value(fixed_seed=True)

        csr_original = self.underlying.discount_curve.short_rate
        csr_del = csr_original / 10.
        csr_new = csr_original + csr_del
        self.update(csr=csr_new)
        value_new = self.present_value(fixed_seed=True)

        rho = (value_new - value_origin) / csr_del
        self.update(csr=csr_original)

        return round(rho, accuracy)

        
        
        
        
        
        