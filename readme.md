## Get Started
By Monana
大三实习时候写的一个脚本，当时正好学习多线程
文件使用的wind API，如果你是wind机构版就会开放期货交易接口，就可以用这个脚本编写你的策略实时交易
也可以把它小小的修改一下，用于其他行情或者下单API比如数字货币等也可以。
代码比较简洁，扩展性强，核心是线程切换。
## Funtion Implemented

### MoQuantCore.py
* 下单线程：支持python语言自定义策略，可以写各种ML/DL/对冲策略，生成下单信号全局变量ordered就可以
* 查询线程：比如持仓/头寸/资金等，只要你交易API支持。
* 订单监控线程：接受下单信号，负责查询你的下单是否成交。

### accountSystem.py
创建的模拟仓账户，已经烂尾，可自行完善。