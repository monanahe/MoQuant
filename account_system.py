#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 1 09:56:49 2017

@author: monana
"""

import datetime
import tushare
import MoQuantHead

import pandas as pd
class account(threading.Thread):
    def __init__(self,account_name,account_id,init_money=1000000):
        
        threading.Thread.__init__(self)
        self.threadID=3
        self.__running=threading.Event()
        self.__running.set()
        
        
        self.account_name=account_name
        self.account_id=account_id
        self.money=init_money
        self.position=pd.DataFrame(columns=['security_id','amount','last_price','total_price'])
        self.capital=pd.DataFrame(columns=['money','profit'])
        self.order=pd.DataFrame(columns=['order_time','security_id','trade_side','trade_price','total_price'])
    def run(self,):
        while(self.__running.is_set())
        if not len(self.position)=0:
            for stock_name in self.position['security_id'].values.tolist()[0]:
                last_price_list[i]=ts.get_realtime_quotes(stock_name)
                self.position['security_id']
    def Position(self,):
        pass
    def Order(self,security_id,amount,trade_side,price):
        if trade_side=='buy' or 'Buy' or 'BUY':
            self.money=self.money-amount*price
            this_order=pd.DataFrame({'security_id':[security_id],'amount':[amount],'trade_side':[trade_side],'price':[price]})
            self.position=self.position.append(this_order)
        if trade_side=='sell':
            pass
        print('Order succeed')
             
    def run(self):
        pass
    def stop(self):
        self.__running.clear()# 将线程从暂停状态恢复, 如何已经暂停的话
        print(str(self.threadID)+' is stopped.')  
        
        
        
        
account1=account('Monana','2')
p=account1.position
account1.capital
account1.Order('600230.SH',300,'buy',2.56)
this_order=pd.DataFrame({'security_id':['232'],'amount':[100],'trade_side':['buy'],'price':[9.22]})