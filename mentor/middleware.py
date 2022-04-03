from functools import wraps

import jwt
# from firebase_admin import auth
from flask import request

from mentor.account.models import Account


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 401
        try:
           
            decoded_token = jwt.decode(request.headers['authorization'], options={"verify_signature": False})
            # decoded_token = auth.verify_id_token(request.headers['authorization'])
            request.decoded_token = decoded_token
            request.account = get_or_create_account(decoded_token['email'])
        except Exception as e:
            return {'message': 'Invalid token provided.'}, 401
        return f(*args, **kwargs)

    return wrap


def get_or_create_account(email):
    account = Account.query.filter_by(email=email).first()
    if account is None:
        account = Account(email=email).save()
    return account
