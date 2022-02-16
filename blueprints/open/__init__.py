from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user

from models import User
from passlib.hash import argon2

bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/')
def index():
    return render_template("index.html")


@bp_open.get('/')
def login_get():
    return render_template('index.html')


@bp_open.post('/')
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Wrong email or password')
        return redirect(url_for('bp_open.index'))

    if not argon2.verify(password, user.password):
        flash('Wrong email or password')
        return redirect(url_for('bp_open.index'))

    login_user(user)
    user.online = True

    from app import db
    db.session.commit()
    return redirect(url_for('bp_user.user_get'))


@bp_open.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_open.post('/signup')
def signup_post():
    name = request.form['name']
    email = request.form.get('email')
    password = request.form['password']
    hashed_password = argon2.using(rounds=10).hash(password)
    from controllers.user_controller import generate_rsa_keys
    public_key = generate_rsa_keys(name)
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address is already in use")
        return redirect(url_for('bp_open.signup_get'))

    new_user = User(name=name, email=email, password=hashed_password, public_key=public_key)

    from app import db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('bp_open.login_get'))
