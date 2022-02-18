from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import logout_user, login_required, current_user

from controllers.message_controller import create_message, get_user_messages, decrypt_message
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
    return render_template('message.html', receiver=receiver)


@bp_user.post('/message/')
def message_post():
    data = request.get_json()
    data = jsonify(data)
    title = data.get_data()
    receiver_id = request.form['user_id']

    create_message(title, title, receiver_id)
    return redirect(url_for('bp_user.user_get'))


@bp_user.get('/mailbox')
def mailbox_get():
    messages = get_user_messages()
    return render_template('mailbox.html', messages=messages)


@bp_user.get('/user_pubkey/<user_id>')
def pubkey_get(user_id):
    user_id = int(user_id)
    pubkey = get_public_key_by_id(user_id)
    return pubkey


@bp_user.get('/messages')
def get_messages():
    messages = get_user_messages()
    msg = messages[0]
    return json.dumps(str(msg))
