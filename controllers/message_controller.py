from flask_login import current_user

from controllers.user_controller import get_user_by_id


def create_message(title, body, receiver_id, aes_rsa):
    from models import Message
    user = current_user
    message = Message(title=title, body=body, sender_id=user.id, aes_rsa=aes_rsa)
    receiver_id = int(receiver_id)
    receiver = get_user_by_id(receiver_id)

    message.receivers.append(receiver)
    from app import db
    db.session.add(message)
    db.session.commit()


def get_aes_message():
    from models import Message
    return Message.query.filter(Message.read == 0).filter(Message.aes_rsa).first()


def get_user_messages():
    return current_user.recv_messages


def get_unread_msg_count():
    user = current_user
    msg_count = 0

    for msg in user.recv_messages:
        if not msg.read:
            msg_count += 1

    return msg_count
