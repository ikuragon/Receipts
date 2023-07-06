from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, IntegerField, TextAreaField, SubmitField



class RegistrationForm(FlaskForm):
    username = StringField(validators=[validators.DataRequired(), validators.Length(min=4, max=50)])
    email = StringField(validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField(validators={validators.DataRequired(),
                                         validators.EqualTo('confirm_password',
                                                            message='Password must match')})
    confirm_password = PasswordField()


class LoginForm(FlaskForm):
    username = StringField(validators=[validators.DataRequired(), validators.Length(min=4, max=50)])
    password = PasswordField(validators=[validators.DataRequired()])


class AddReceiptForm(FlaskForm):
    name_of_receipt = StringField(validators=[validators.DataRequired(), validators.Length(max=100)])
    about_of_receipt = StringField(validators=[validators.DataRequired()])
    ingredients = StringField(validators=[validators.DataRequired()])
    kilocalories = StringField(validators=[validators.DataRequired()])


class RatingForm(FlaskForm):
    rate = IntegerField('Оценка:', validators=[validators.DataRequired()])
    comment = TextAreaField('Комментарий:')
    submit = SubmitField('Отправить')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Адрес электронной почты', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Подтвердить')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль', validators=[validators.DataRequired()])
    submit = SubmitField('Подтвердить')
