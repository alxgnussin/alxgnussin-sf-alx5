from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, TextAreaField


class CartForm(FlaskForm):
    client_name = StringField(
        'Имя пользователя ',
        [
            validators.InputRequired(message='Необходимо ввести имя'),
            validators.Length(min=4, max=20, message='От 4-х до 20-ти символов')
        ]
    )
    client_mail = StringField(
        'Электронная почта ',
        [
            validators.Email(message='Введенный адрес некорректен'),
            validators.DataRequired(message='Поле не должно быть пустым')
        ]
    )
    client_phone = StringField(
        'Телефонный номер ',
        [
            validators.DataRequired(message='Поле не должно быть пустым'),
            validators.Length(min=11, message='не менее 11 цифр')
        ]
    )
    client_address = TextAreaField(
        'Адрес доставки ',
        [validators.DataRequired(message='Необходимо указать адрес доставки')]
    )


class RegistrationForm(FlaskForm):
    user_name = StringField(
        'Имя пользователя ',
        [
            validators.InputRequired(message='Необходимо ввести имя'),
            validators.Length(min=4, max=20, message='От 4-х до 20-ти символов')
        ]
    )
    user_password = PasswordField(
        'Пароль ',
        [
            validators.DataRequired(message='Необходимо ввести пароль'),
            validators.Length(min=8, message='Не менее 8-ми символов!')
        ]
    )
    confirm_password = PasswordField(
        'Повторите пароль ',
        [
            validators.DataRequired(message='Не введен пароль для проверки'),
            validators.EqualTo('user_password', message='Пароли не совпадают!')
        ]
    )
    user_email = StringField(
        'Электронная почта ',
        [
            validators.Email(message='Введенный адрес некорректен'),
            validators.DataRequired(message='Поле не должно быть пустым')
        ]
    )
    user_phone = StringField(
        'Телефонный номер ',
        [
            validators.DataRequired(message='Поле не должно быть пустым'),
            validators.Length(min=11, message='не менее 11 цифр')
        ]
    )
    user_address = TextAreaField('Ваш адрес: ')


class LoginForm(FlaskForm):
    email = StringField(
        'Электронная почта ',
        [
            validators.Email(message='Введенный адрес некорректен'),
            validators.DataRequired(message='Поле не должно быть пустым')
        ]
    )
    password = PasswordField(
        'Пароль ',
        [
            validators.DataRequired(message='Необходимо ввести пароль'),
            validators.Length(min=8, message='Не менее 8-ми символов!')
        ]
    )