# -*- coding: utf-8 -*-
"""
从优矿下载沪深300数据（2015-2018）
"""

df1 = DataAPI.MktEqudGet(secID=u"",ticker=stock_list,tradeDate=u"",
                         beginDate=u"20150101",endDate=u"",isOpen="",
                         field=u"",pandas="1")

stock_list = list(DataAPI.IdxConsGet(secID=u"",ticker=u"000300",isNew=u"",
                                     intoDate=u"20141231",field=u""
                                     ,pandas="1").consTickerSymbol)

df1.to_csv('HS300_dailydata_2015_2018.csv')