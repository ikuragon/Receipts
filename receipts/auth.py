from main import *
from forms import *
from models import User
from flask_mail import Message
from flask import render_template, flash, redirect, url_for, session, request
from werkzeug.security import generate_password_hash, check_password_hash


@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'forgot_password', 'reset_password']
    if request.endpoint not in allowed_routes and 'logged_in' not in session:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_user or existing_email:
            flash('Данное имя пользователя или почта уже заняты', 'error')
            return render_template('register.html', form=form)
        user = User(username=form.username.data, email=form.email.data,
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_password_email(user)
            flash('Инструкции по сбросу пароля были отправлены на вашу почту', 'success')
            return redirect(url_for('login'))
        else:
            flash('Пользователь с таким адресом электронной почты не существует', 'error')
    return render_template('forgot_password.html', form=form)


def send_reset_password_email(user):
    token = user.get_reset_token()
    msg = Message('Сброс пароля', sender='recepty15@gmail.com', recipients=[user.email])
    msg.body = f'''Для сброса пароля, перейдите по следующей ссылке:
    {url_for('reset_password', token=token, _external=True)}
    Если вы не запрашивали сброс пароля, проигнорируйте это письмо.
    '''
    mail.send(msg)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Ссылка на сброс пароля недействительна', 'error')
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        user.reset_token = None
        db.session.commit()
        flash('Пароль успешно сброшен.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form, token=token)


def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('index'))
