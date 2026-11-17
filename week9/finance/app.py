import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create transactions table if it does not exist yet
db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, type TEXT NOT NULL, transacted TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")
db.execute("CREATE INDEX IF NOT EXISTS transactions_user_id_index ON transactions (user_id)")
db.execute("CREATE INDEX IF NOT EXISTS transactions_symbol_index ON transactions (symbol)")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])
    stocks = []
    total_value = 0
    for row in rows:
        quote = lookup(row["symbol"])
        if quote is None:
            continue
        price = quote["price"]
        total = price * row["total_shares"]
        total_value += total
        stocks.append({"symbol": quote["symbol"], "name": quote["name"],
                      "shares": row["total_shares"], "price": price, "total": total})
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    return render_template("index.html", stocks=stocks, cash=cash, total=total_value + cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must provide symbol", 400)
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 400)
        if not shares:
            return apology("must provide shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if shares <= 0:
            return apology("shares must be a positive integer", 400)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        cost = quote["price"] * shares
        if cost > cash:
            return apology("cannot afford", 400)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], shares, quote["price"], "BUY")
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
        flash("Bought")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT symbol, shares, price, type, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC, id DESC", session["user_id"])
    return render_template("history.html", transactions=rows)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to the user account (personal touch)."""
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount:
            return apology("must provide amount", 400)
        try:
            amount = float(amount)
        except ValueError:
            return apology("amount must be a positive number", 400)
        if amount <= 0:
            return apology("amount must be a positive number", 400)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        flash("Cash added")
        return redirect("/")
    else:
        return render_template("add_cash.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 400)
        return render_template("quoted.html", name=quote["name"], price=quote["price"], symbol=quote["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must provide password confirmation", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)
        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                                 username, generate_password_hash(password))
        except ValueError:
            return apology("username already exists", 400)
        session["user_id"] = user_id
        flash("Registered")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must select a stock", 400)
        if not shares:
            return apology("must provide shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if shares <= 0:
            return apology("shares must be a positive integer", 400)
        owned = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        total_shares = owned[0]["total_shares"]
        if total_shares is None or shares > total_shares:
            return apology("too many shares", 400)
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 400)
        proceeds = quote["price"] * shares
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], -shares, quote["price"], "SELL")
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", proceeds, session["user_id"])
        flash("Sold")
        return redirect("/")
    else:
        stocks = db.execute(
            "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])
        return render_template("sell.html", stocks=stocks)
