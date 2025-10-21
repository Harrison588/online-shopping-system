from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for sessions

# 🛍 Sample product data
products = [
    {"id": 1, "name": "Nike Air Max", "price": 3500, "image": "/static/nike air max.jpg"},
    {"id": 2, "name": "Adidas Hoodie", "price": 2500, "image": "/static/adidas hoodie.jpg"},
    {"id": 3, "name": "Apple Watch", "price": 12000, "image": "/static/apple watch.jpg"}
]

# 🛒 Cart storage
cart = []

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', products=products, username=session['username'])
    return redirect(url_for('register'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session['username'] = request.form["name"]
        session['email'] = request.form["email"]
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    for product in products:
        if product["id"] == product_id:
            cart.append(product)
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if item["id"] != product_id]
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    total = sum(item["price"] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout')
def checkout():
    total = sum(item["price"] for item in cart)
    return render_template('checkout.html', cart=cart, total=total)

@app.route("/payment", methods=["GET", "POST"])
def payment():
    amount = sum(item["price"] for item in cart)
    if request.method == "POST":
        phone = request.form["phone"]
        return render_template("success.html", phone=phone, amount=amount)
    return render_template("payment.html", amount=amount)

if __name__ == "__main__":
    app.run(debug=True)