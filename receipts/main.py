from flask import Flask, render_template, flash, redirect, url_for, session, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receipts.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'recepty15@gmail.com'
app.config['MAIL_PASSWORD'] = 'ktvkmmxsierwcrvz'
app.secret_key = 'passkeey'
db = SQLAlchemy(app)
mail = Mail(app)
