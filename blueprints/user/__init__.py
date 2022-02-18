from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import logout_user, login_required, current_user

from controllers.message_controller import create_message, get_user_messages, get_aes_message
from controllers.user_controller import get_all_but_current_user, get_user_by_id, get_public_key_by_id
import json


bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/profile')
@login_required
def user_get():
    users = get_all_but_current_user()
    return render_template("user.html", users=users)


@bp_user.get('/logout')
def logout_get():
    user = current_user
    user.online = False

    from app import db
    db.session.commit()
    logout_user()
    return redirect(url_for('bp_open.index'))


@bp_user.get('/message/<user_id>')
def message_get(user_id):
    user_id = int(user_id)
    receiver = get_user_by_id(user_id)
    receiver_publickey = get_public_key_by_id(receiver.id)
    return render_template('message.html', receiver=receiver, receiver_publickey=receiver_publickey)


@bp_user.post('/message')
def message_post():
    title = request.form['cipher_title']
    body = request.form['cipher_body']
    aes_rsa = request.form['encrypted_aes']
    receiver_id = request.form['user_id']
    create_message(title, body, receiver_id, aes_rsa)
    return redirect(url_for('bp_user.user_get'))


@bp_user.get('/mailbox')
def mailbox_get():
    messages = get_user_messages()
    aes_rsa = get_aes_message()
    return render_template('mailbox.html', messages=messages, aes_rsa=aes_rsa)


@bp_user.get('/messages')
def get_messages():
    messages = get_user_messages()
    msg = messages[0]
    return render_template('Mailbox.html')
