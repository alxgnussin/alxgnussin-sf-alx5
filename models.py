from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


orders_meals = db.Table(
    'p5_orders_meals',
    db.Column('meals_id', db.Integer, db.ForeignKey('p5_meals.id')),
    db.Column('orders_id', db.Integer, db.ForeignKey('p5_orders.id'))
)


class User(db.Model):
    __tablename__ = 'p5_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    mail = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.Text, nullable=True)

    orders = db.relationship('Order', back_populates='user')


class Meal(db.Model):
    __tablename__ = 'p5_meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Numeric(asdecimal=False), nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(32), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('p5_categories.id'))

    category = db.relationship('Category', back_populates='meals')
    orders = db.relationship('Order', secondary=orders_meals, back_populates='meals')


class Category(db.Model):
    __tablename__ = "p5_categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(24), nullable=False)

    meals = db.relationship('Meal', back_populates='category')


class Order(db.Model):
    __tablename__ = 'p5_orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.String(10), nullable=False)
    order_sum = db.Column(db.Numeric(asdecimal=False), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.Text, nullable=False)
    mail = db.Column(db.String(30), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('p5_users.id'))

    user = db.relationship('User', back_populates='orders')
    meals = db.relationship('Meal', secondary=orders_meals, back_populates='orders')