import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Florist, Flower, User
from shop.forms import RegistrationForm, LoginForm, SearchForm, CheckoutForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods= ['GET', 'POST'])

@app.route("/home", methods= ['GET', 'POST'])
def home():
	form = SearchForm()
	search = SearchForm(request.form)
	search_string = ""
	if request.method == 'POST':
		search_string = search.items['search']
		flowers = Flower.query.filter_by(Flower.title == search_string).first()
		return render_template('home.html', flowers=flower, form=form)
	return render_template('home.html', flowers = Flower.query.all(), title='Home')	

@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/orderasc")
def orderasc():
	return render_template('home.html', flowers = Flower.query.order_by("price"), title='Home')

@app.route("/orderdesc")
def orderdesc():
	return render_template('home.html', flowers = Flower.query.order_by("price")[::-1], title='Home')

@app.route("/flower/<int:flower_id>")
def flower(flower_id):
	flower = Flower.query.get_or_404(flower_id)
	return render_template('flower.html', flower=flower) #title=book.title

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)

        db.session.commit()
        flash('Your account has been created.  You can now log in.')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
    	#user = User(forename=form.forename.data,surname=form.surname.data)
    	session["cart"] = []
    	return redirect(url_for('thankyou'))
    return render_template('checkout.html', title='Checkout', form=form)
    	
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')

        return render_template('login.html', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
		db.session.commit()
		session.clear()
		logout_user()
		return redirect(url_for('home'))

@app.route("/add_to_cart/<int:flower_id>")
def add_to_cart(flower_id):
	if "cart" not in session:
		session["cart"] = []
	session["cart"].append(flower_id)
	flash("The flower is added to your shopping cart!")
	return redirect("/cart")

@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
    if "cart" not in session:
        flash('There is nothing in your cart.')
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        cart = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            flower = Flower.query.get_or_404(item)

            total_price += flower.price
            if flower.id in cart:
                cart[flower.id]["quantity"] += 1
            else:
                cart[flower.id] = {"quantity":1, "title": flower.title, "price":flower.price}
            total_quantity = sum(item['quantity'] for item in cart.values())


        return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, total_quantity = total_quantity)

    return render_template('cart.html')

@app.route("/delete_flower/<int:flower_id>", methods=['GET', 'POST'])
def delete_flower(flower_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].remove(flower_id)

    flash("The item has been removed from your shopping cart!")

    session.modified = True

    return redirect("/cart")

@app.route("/add_to_wishlist/<int:flower_id>")
def add_to_wishlist(flower_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].append(flower_id)
    flash("The item has been added to your wishlist")
    return redirect("/wishlist")

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist_display():
    if "wishlist" not in session:
        flash('Your wishlist is empty.')
        return render_template("wishlist.html", display_wishlist = {}, total = 0)
    else:
        items = session["wishlist"]
        wishlist = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            flower = Flower.query.get_or_404(item)

            total_price += flower.price
            if flower.id in wishlist:
                wishlist[flower.id]["quantity"] += 1
            else:
                wishlist[flower.id] = {"quantity":1, "title": flower.title, "price":flower.price}
            total_quantity_wishlist = sum(flower_id['quantity'] for flower_id in wishlist.values())

        return render_template("wishlist.html", title= "Your Shopping Cart", display_wishlist = wishlist, total = total_price, total_quantity_wishlist = total_quantity_wishlist)

@app.route("/delete_flower_wishlist/<int:flower_id>", methods=['GET', 'POST'])
def delete_flower_wishlist(flower_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].remove(flower_id)

    flash("The item has been removed from your wishlist")
    session.modified = True
    return redirect("/wishlist")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html", title='Thank You')

