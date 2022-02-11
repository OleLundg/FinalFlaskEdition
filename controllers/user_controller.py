from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
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


def rsa_encrypt(rsa_key_name, msg):
    # recipient_key = RSA.importKey(open(f'./rsa_keys/{rsa_key_name}.pem').read())
    # recipient_key_pem = RSA.importKey(rsa_key_name)
    cipher_rsa = PKCS1_OAEP.new(rsa_key_name)
    return cipher_rsa.encrypt(msg)


def rsa_decrypt(cipher, recipient_key):
    if type(recipient_key) != RsaKey:
        recipient_key = RSA.importKey(open(f'./rsa_keys/{recipient_key}.pem').read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    return cipher_rsa.decrypt(cipher)
