# -*- coding: utf-8 -*-
# Python 3.7.7 required
import os
from datetime import date

from flask import Flask, render_template, request, redirect, session, url_for

from models import db, Meal, User, Order
from operations import get_meals_for_main
from forms import RegistrationForm, LoginForm, CartForm

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def render_index():
    return render_template('main.html', offers=get_meals_for_main(db))


@app.route('/cart/', methods=['GET', 'POST'])
def render_cart():
    meals = []

    if 'cart' not in session:
        session['cart'] = []
    for i in session['cart']:
        meal = db.session.query(Meal).get(i)
        meals.append(meal)

    cart_form = CartForm()
    if not cart_form.is_submitted() and session['is_auth']:
        client = db.session.query(User).get(session['user_id'])
        cart_form.client_name.data = client.name
        cart_form.client_address.data = client.address
        cart_form.client_mail.data = client.mail
        cart_form.client_phone.data = client.phone

    if cart_form.validate_on_submit():
        order = Order(
            order_date=date.today().isoformat(),
            order_sum=session['total'],
            phone=cart_form.client_phone.data,
            address=cart_form.client_address.data,
            mail=cart_form.client_mail.data,
            user_id=session['user_id']
        )

        for meal_id in session['cart']:
            meal = db.session.query(Meal).get(meal_id)
            order.meals.append(meal)

        db.session.add(order)
        db.session.commit()

        return redirect(url_for('render_ordered'))

    return render_template('cart.html', meals=meals, form=cart_form)


@app.route('/account/')  # личный кабинет
def render_account():
    return render_template('account.html')


@app.route('/register/', methods=['GET', 'POST'])
def render_register():
    message = 'Создайте свой аккаунт'
    new_user_form = RegistrationForm()
    if new_user_form.validate_on_submit():
        new_user_name = new_user_form.user_name.data
        new_user_password = new_user_form.user_password.data
        new_user_mail = new_user_form.user_email.data
        new_user_phone = new_user_form.user_phone.data
        new_user_address = new_user_form.user_address.data

        record_is_present = db.session.query(User).filter(User.mail == new_user_mail).first()
        if record_is_present is None:
        
            user = User(
                name=new_user_name,
                password=new_user_password,
                mail=new_user_mail,
                phone=new_user_phone,
                address=new_user_address
            )

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('render_index'))
        else:
            message = 'Пользователь с такой почтой уже зарегистрирован'

    return render_template('register.html', form=new_user_form, message=message)


@app.route('/login/', methods=['GET', 'POST'])
def render_login():
    login_form = LoginForm()
    message = "Войдите, чтобы управлять"
    if login_form.validate_on_submit():
        mail = login_form.email.data
        password = login_form.password.data

        user = db.session.query(User).filter(User.mail == mail).first()
        if user and user.password == password:
            session['is_auth'] = True
            session['user_id'] = user.id
            # session['user_mail'] = user.mail

            return redirect(url_for('render_account'))

        else:
            message = "Пользователь не найден. Повторите ввод или зарегистрируйтесь"

    return render_template('login.html', form=login_form, message=message)


@app.route('/logout/', methods=['GET'])
def render_logout():
    if request.method == 'GET':
        session.clear()
    return redirect(url_for('render_index'))


@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')


@app.route('/add_to_cart/', methods=['POST'])
def render_add():
    meal_id = request.form.get('meal_id')
    if 'cart' not in session:
        session['cart'] = []
        session['total'] = 0

    cart = session['cart']
    cart.append(meal_id)
    session['cart'] = cart

    total = session['total']
    meal = db.session.query(Meal).get(meal_id)
    total += meal.price
    session['total'] = total

    return redirect(url_for('render_cart') + '?action=add')


@app.route('/delete_from_card/', methods=['POST'])
def render_delete():
    meal_id = request.form.get('meal_id')

    cart = session['cart']
    cart.remove(meal_id)
    session['cart'] = cart

    total = session['total']
    meal = db.session.query(Meal).get(meal_id)
    total -= meal.price
    session['total'] = total

    return redirect(url_for('render_cart') + '?action=remove')


if __name__ == '__main__':
    app.run(debug=True)
