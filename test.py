from flask import Flask, render_template, request, url_for, redirect, session,flash
from datetime import datetime, timedelta
from database import AccountManager
from yahoo_fin import stock_info as si
from stonks import Stonks

app = Flask(__name__)
app.secret_key= 'hello'
app.permanent_session_lifetime = timedelta(days= 5)
am = AccountManager()
now = datetime.utcnow()
stk = Stonks()
email = "jonnysires@yahoo.com"

results = am.watchlist(email)
stonk_day_change = []
for result in results:
            
            try:
                value = si.get_quote_table(result)
                value2 = value['Open']
                stonk_day_change.append(value2)
                print(value2)
            except:
                stonk_day_change.append(0)
print( stonk_day_change)