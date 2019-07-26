
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:46:35 2017

@author: thinkpadx1
"""

import wtool #Cope with wind API
import MoQuantHead	#This is all the libraries and preference settings.

#线程1：订单监控
class worder_moniter(threading.Thread): 
    
    def __init__(self): 
        threading.Thread.__init__(self)
        global ordered
        self.threadID=1
        self.__running=threading.Event()
        self.__running.set()
        
    def run(self):
        while(self.__running.is_set()):
            if(ordered.is_set()):
                print("订单已提交，详情如下：")
                time.sleep(2)#给一个短暂延时，希望返回订单是否“已成”
                Query=w.tquery('Order','LogonID=1;WindCode=I1801.DCE')
                last_Query_df=wtodf_order(Query).iloc[-1]
                print(last_Query_df.T)
                last_Query_df.to_csv('Order_list.csv','a+')
                ordered.clear()#一次交易处理完毕
        
    def stop(self):
        self.__running.clear()# 将线程从暂停状态恢复, 如何已经暂停的话
        print(str(self.threadID)+' is stopped.')

#线程2：信号事件产生
class worder_generate(threading.Thread): 
    
    def __init__(self): 
        threading.Thread.__init__(self)
        global ordered
        self.__running=threading.Event()
        self.__running.set()
        self.threadID=2
        global position_check
        
    def run(self):
        #设置策略基本参数
        security_code='I1801.DCE'
        frequency=60 #[60,5*60,10*60]
        market_close_time=' 14:55:00 2017'
        order_amount=1
        print('[最高价] ','[最低价] ','[现价] ','[现量] ','多头价 ','空头价')
        while(self.__running.is_set()):
            #获取实时数据
            real=w.wsq(security_code,'rt_high,rt_low,rt_last,rt_last_vol')
            
            '''
            基本数据
            '''
            high=real.Data[0][0]
            low=real.Data[1][0]
            last=real.Data[2][0]
            vol=real.Data[3][0]

            '''
            策略部分
            '''
            useStrategy=False#是否使用策略
            #策略参数#
            #设置多空上下轨价格线
            long_price=563
            short_price=550
            order_price=last
            #设置价格触发信号
            signal=last>=long_price or last<short_price 
            
            if(signal&useStrategy):
            #向仓位检查函数发信号，进行仓位更新
                position_check.set()
                long_position=check.long_position
                short_position=check.short_position
            #仓位更新完毕
            
            #策略调仓部分#
                if last>=long_price: #多头
                        w.torder(security_code,'buy',str(order_price),str(order_amount),'OrderType= LMT;LogonID=1')
                        if short_position:
                            w.torder(security_code,'cover',str(order_price),str(order_amount),'OrderType= LMT;LogonID=1')
                        
                elif last<short_price: #空头
                    w.torder(security_code,'short',str(order_price),str(order_amount),'OrderType= LMT;LogonID=1')
                    if long_position:
                        w.torder(security_code,'sell',str(order_price),str(order_amount),'OrderType= LMT;LogonID=1')

                ordered.set()#已经调仓，通知订单检查线程
                self.frq_wait(frequency)
                '''
                策略部分结束
                '''
#            buy cover 多开 空平  都是看多
#            short sell 空开 多平 都是看空

            #简单的测试策略
#            if last>553:
#                w.torder(security_code,'sell',str(order_price),str(order_amount),'OrderType= LMT;LogonID=1')
#                ordered.set()
#                self.frq_wait(frequency)
#
#            elif last<551:
#                w.torder(security_code,'sell',str(order_price),str(order_amount),'OrderType= LMT;LogonID=1')
#                ordered.set()
#                self.frq_wait(frequency)

            time.sleep(3)#实时数据刷新时间
            print(real.Data,long_price,short_price)
			
    def stop(self):
        self.__running.clear()# 将线程从暂停状态恢复, 如何已经暂停的话
        print(str(self.threadID)+' is stopped.')   
		
    def frq_wait(self,seconds):
        i=0
        while(i<seconds):
            i=i+1
            sys.stdout.write('\r'+'下一个调仓周期：'+str(i)+'/'+str(seconds)+'秒')
            sys.stdout.flush()
            time.sleep(1)
       
#线程3：订单查询回调函数（该线程全程运行无需中断）
class worder_check(threading.Thread): 
    
    def __init__(self): 
        threading.Thread.__init__(self)
        self.threadID=3
        self.__running=threading.Event()
        self.__running.set()
        self.long_position=0
        self.short_position=0
        global position_check
        
    def run(self):
        pass
		
    def stop(self):
        self.__running.clear()# 将线程从暂停状态恢复, 如何已经暂停的话
        print(str(self.threadID)+' is stopped.')    
        
    #查询资金头寸
    @property
    def C(self):
        Capital=w.tquery('Capital','LogonID=1')
        wprint(Capital)
        self.Capital=Capital
        return Capital
		
    #查询持仓
    @property
    def P(self):
        Position=w.tquery('Position','LogonID=1')
        Position=wtodf_Position(Position)
        if not len(Position.columns.values):#仓位不为空
        #逐一打印持仓情况
            for i in range(0,len(Position)):
                print(Position.iloc[i].T)
                if Position['TradeSide'].iat[0]=='Buy':
                    self.long_position=Position.iloc[i]
                elif Position['TradeSide'].iat[0]=='Short':
                    self.short_position=Position.iloc[i]
        else: print('空仓观望中~')
        return Position

    #查询今日订单
    def O(self):
        O=w.tquery('Order','LogonID=1;WindCode=I1801.DCE')
        O=wtodf_order(O)
        print(O)
        
if __name__ == '__main__':
            
	ordered=threading.Event()
	position_check=threading.Event()

	thread1=worder_moniter()
	thread2=worder_generate()
	check=worder_check()

	check.start()
	thread1.start()
	thread2.start()


