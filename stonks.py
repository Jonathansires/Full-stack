from yahoo_fin import stock_info
from database import AccountManager 

si = stock_info
am = AccountManager()

class Stonks:
    def __init__(self):
        yes=1


    def get_stonk_price(self,results):
        stonk_price_list=[]
        for stock in results:
            try:
                stonk_price_list.append(si.get_live_price(stock))
            except Exception as e:
                stonk_price_list.append(0)
        return stonk_price_list
    
    def get_price_change(self,results ):
        stonk_day_change = []
        for result in results:
            
            try:
                value = si.get_quote_table(result)
                value2 = value['Open']
                stonk_day_change.append(value2)
            except:
                stonk_day_change.append(0)
        return stonk_day_change
           


