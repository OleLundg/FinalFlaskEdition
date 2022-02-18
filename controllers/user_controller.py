from Crypto.PublicKey import RSA
from flask_login import current_user


def get_all_but_current_user():
    from models import User
    user = current_user
    return User.query.filter(User.id != user.id).all()


def get_all_users():
    from models import User
    return User.query.all()


def get_public_key_by_id(user_id):
    from models import User
    return User.query.filter(User.id == user_id).filter(User.public_key).first()


def get_user_by_id(user_id):
    from models import User
    return User.query.filter(User.id == user_id).first()


def generate_rsa_keys(key_name, key_size=2048):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    with open(f'./rsa_keys/{key_name}_private.pem', 'wb') as out_file:
        out_file.write(private_key)
    public_key = key.public_key().export_key()
    return public_key

