# -*- coding: utf-8 -*-

# market_environment.py

class market_environment(object):
    """
    初始化估值的市场环境相关信息
    """
    def __init__(self, name, pricing_date):
        self.name = name
        self.pricing_date = pricing_date
        self.constants = {}
        self.lists = {}
        self.curves = {}
        
    
    def add_constant(self, key, constant):
        self.constants[key] = constant
       
        
    def get_constant(self, key):
        return self.constants[key]
        
    
    def add_list(self, key, constant):
        self.lists[key] = constant
       
        
    def get_list(self, key):
        return self.lists[key]
    
    
    def add_curve(self, key, constant):
        self.curves[key] = constant
       
        
    def get_curve(self, key):
        return self.curves[key]
    
    
    def add_environment(self, env):
        """
        如果某个值已经存在，则进行覆盖
        """
        for key in env.constants:
            self.constants[key] = env.constants[key]
            
        for key in env.lists:
            self.lists[key] = env.lists[key] 
            
        for key in env.curves:
            self.curves[key] = env.curves[key]