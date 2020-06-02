from flask import Blueprint, redirect, url_for, render_template, session, request
from werkzeug.security import generate_password_hash, check_password_hash

from forms import RegistrationForm, LoginForm
from models import db, User

bp = Blueprint('auth', __name__)


@bp.route('/register/', methods=['GET', 'POST'])
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
                password=generate_password_hash(new_user_password),
                mail=new_user_mail,
                phone=new_user_phone,
                address=new_user_address
            )
            print(user.password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('store.render_index'))
        else:
            message = 'Пользователь с такой почтой уже зарегистрирован'

    return render_template('register.html', form=new_user_form, message=message)


@bp.route('/login/', methods=['GET', 'POST'])
def render_login():
    login_form = LoginForm()
    message = "Войдите, чтобы управлять"
    if login_form.validate_on_submit():
        mail = login_form.email.data
        password = login_form.password.data

        user = db.session.query(User).filter(User.mail == mail).first()
        if user and check_password_hash(user.password, password):
            session['is_auth'] = True
            session['user_id'] = user.id

            return redirect(url_for('store.render_account'))

        else:
            message = "Пользователь не найден. Повторите ввод или зарегистрируйтесь"

    return render_template('login.html', form=login_form, message=message)


@bp.route('/logout/', methods=['GET'])
def render_logout():
    if request.method == 'GET':
        session.clear()
    return redirect(url_for('store.render_index'))
