import json

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from flask_login import current_user

from controllers.user_controller import get_user_by_id, rsa_encrypt, rsa_decrypt


def create_message(title, body, receiver_id):
    from models import Message
    user = current_user
    receiver_id = int(receiver_id)
    receiver = get_user_by_id(receiver_id)
    body = body
    message = Message(body=body, sender_id=user.id)

    message.receivers.append(receiver)
    from app import db
    db.session.add(message)
    db.session.commit()


def get_user_messages():
    return current_user.recv_messages


def get_unread_msg_count():
    user = current_user
    msg_count = 0

    for msg in user.recv_messages:
        if not msg.read:
            msg_count += 1

    return msg_count


def aes_encrypt(msg):
    key = get_random_bytes(16)
    cipher_aes = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(msg.encode('utf-8'))

    return key, ciphertext, cipher_aes.nonce, tag


def aes_decrypt(aes_key, ciphertext, nonce, tag):
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
    decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return decrypted_data.decode('utf-8')


def encrypt_message(msg, recipient_rsa_key_name):
    aes_key, aes_cipher, aes_nonce, aes_tag = aes_encrypt(msg)
    encrypted_aes_key = rsa_encrypt(recipient_rsa_key_name, aes_key)

    return encrypted_aes_key, aes_nonce, aes_tag, aes_cipher


def decrypt_message(private_key_name, encrypted_data):
    encrypted_aes_key, aes_nonce, aes_tag, aes_cipher = encrypted_data
    aes_key = rsa_decrypt(encrypted_aes_key, private_key_name)
    plaintext = aes_decrypt(aes_key, aes_cipher, aes_nonce, aes_tag)

    return plaintext
