# -*- coding: utf-8 -*-

# valuation_class.py

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
            

    def update(self, initial_value=None, volatility=None, strike=None, maturity=None):
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

    def vega(self, interval=0.01, accuracy=4):
        if interval<self.underlying.volatility/50.0:
            interval = self.underlying.volatility/50.
        
        value_left = self.present_value(fixed_seed=True)
        
        vola_del = self.underlying.volatility + interval
        self.underlying.update(volatility=vola_del)
        
        value_right = self.present_value(fixed_seed=True)
        
        self.underlying.update(volatility=vola_del - interval)
        
        vega = (value_right - value_left)/interval
        
        return round(vega, accuracy)
        
        
        
        
        
        
        
        
        