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

tickers = []
tickers.append(si.tickers_dow())
tickers.append(si.tickers_nasdaq())
tickers.append(si.tickers_sp500())
tickers.append(si.tickers_niftybank())
tickers.append(si.tickers_other())


def __repr__(self):
     return '<task %r>' % self.id

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/account", methods=['GET', 'POST'])
def account():
    if 'user' in session:
        user = session['user']
        session['money'] = am.get_money(user)
        results = am.watchlist(user)
        stonk_price_list = stk.get_stonk_price(results)
        price_change =stk.get_price_change(results)
        if request.method == 'POST':
            if "add" in request.form:
                stock = request.form['stock']
                if stock != "":
                    am.create_watchlist(user, stock, now)
                else:
                    flash("You need an input.", "info")
            elif "delete" in request.form:
                delete_index = int(request.form['delete_index'])
                if delete_index >= 0 and delete_index < len(results):
                    am.delete_watchlist_item(user, results[delete_index])
                else:
                    flash("Invalid index.", "info")
            elif "refresh" in request.form:
                return redirect(url_for("account"))

            # Reload the watchlist and stock prices after adding or deleting an item
            results = am.watchlist(user)
            stonk_price_list=[]
            price_change =stk.get_price_change(results)
            for stock in results:
                try:
                    stonk_price_list.append(si.get_live_price(stock))
                except Exception as e:
                    stonk_price_list.append(0)
                    flash(f"{stock} is not a valid stock")

        # Render the account page with the updated watchlist and stock prices
        return render_template("account.html", results=results, stonk_price_list=stonk_price_list, tickers=tickers,price_change=price_change)

    else:
         flash("You are not logged in", "info")
         return render_template("login.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        password = request.form['pw']
        fname = am.get_firstname(email)
        
        if am.check_credentials(email, password) == True:

            session['user']= email
            flash("login Success","info")
            return render_template('user.html', email=fname)
        else:
            flash("Account does not exist.","info")
            return render_template("login.html")
    else:
        if "user" in session:
            flash('Already logged in', "info")
            return redirect(url_for('user'))
        
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    if 'user' in session:
        user = session['user']
        fname = am.get_firstname(user)
        
        return render_template("user.html", email=fname)
    else:
         flash("You are not logged in", "info")
         return render_template("login.html")
    
     
@app.route("/logout")
def logout():
    if 'user' in session:
        flash('Logout successful', "info")
        session.pop('user', None)
        session.pop('email', None)
    return redirect(url_for("login"))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        password = request.form['pw']
        if not email.strip() or not fname.strip() or not lname.strip() or not password.strip():
            flash('Please fill in all the required fields.', 'error')
            return redirect(url_for('signup'))
        else:
            if "user" in session:
                flash('Already logged in', "info")
                return redirect(url_for('user'))

            if am.check_email(email) == False:
                am.create_account(fname, lname, email, password)
                flash("Sign up success. Please log in.", "info")
                return redirect(url_for('login'))
            else:
                flash('Email already exists.')
                return redirect(url_for('signup'))

    return render_template('signup.html')

if __name__ == "__main__":
   app.run(host="0.0.0.0")