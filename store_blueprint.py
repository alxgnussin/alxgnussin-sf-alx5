from datetime import date

from flask import Blueprint, render_template, session, redirect, url_for, request

from forms import CartForm
from models import db, User, Meal, Order
from operations import get_meals_for_main

bp = Blueprint('store', __name__)


@bp.route('/')
def render_index():
    return render_template('main.html', offers=get_meals_for_main(db))


@bp.route('/cart/', methods=['GET', 'POST'])
def render_cart():
    meals = []

    if 'cart' not in session:
        session['cart'] = []
    for i in session['cart']:
        meal = db.session.query(Meal).get(i)
        meals.append(meal)

    cart_form = CartForm()
    if not cart_form.is_submitted() and 'is_auth' in session:
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
        session['cart'] = []
        session['total'] = 0

        return redirect(url_for('store.render_ordered'))

    return render_template('cart.html', meals=meals, form=cart_form)


@bp.route('/account/')  # личный кабинет
def render_account():
    orders = db.session.query(Order).filter(Order.user_id == session['user_id']).all()

    order_list = []
    for order in orders:
        meal_list = []
        for meal in order.meals:
            meal_list.append(meal)
        my_dict = {'order_date': order.order_date, 'order_sum': order.order_sum, 'meals': meal_list}
        order_list.append(my_dict)
        print(order.order_date)
    return render_template('account.html', orders=order_list)


@bp.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')


@bp.route('/add_to_cart/', methods=['POST'])
def render_add():
    meal_id = request.form.get('meal_id')

    cart = session.get('cart', [])
    cart.append(meal_id)
    session['cart'] = cart

    total = session.get('total', 0)
    meal = db.session.query(Meal).get(meal_id)
    total += meal.price
    session['total'] = total

    return redirect(url_for('store.render_cart') + '?action=add')


@bp.route('/delete_from_card/', methods=['POST'])
def render_delete():
    meal_id = request.form.get('meal_id')

    cart = session['cart']
    cart.remove(meal_id)
    session['cart'] = cart

    total = session['total']
    meal = db.session.query(Meal).get(meal_id)
    total -= meal.price
    session['total'] = total

    return redirect(url_for('store.render_cart') + '?action=remove')
