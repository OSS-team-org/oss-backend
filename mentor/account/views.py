# -*- coding: utf-8 -*-
"""User views."""
import logging
import json
import random
#push
# from firebase_admin import auth
from flask import Blueprint, request, Response, jsonify
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields
from sqlalchemy import or_
import datetime
import jwt
from flask_bcrypt import Bcrypt
from .models import Account, Role, UserRoles

from .serializers import account_schema, account_schemas, role_schema, role_schemas
# from ..firebase import pb
from mentor.middleware import check_token
# from ..utils import get_account_verification_stage, send_mail

blueprint = Blueprint('account', __name__)
bcrypt = Bcrypt()

@blueprint.route('/api/account/', methods=['GET'])
@check_token
@marshal_with(account_schema)
def get_account_by_token():
    account = request.account
    account.verification_stage = get_account_verification_stage(account)
    # logging.info('Response: {}'.format(account.__dict__) )
    return account


@blueprint.route('/api/accounts/<int:account_id>', methods=['GET'])
@check_token
@marshal_with(account_schema)
def get_account_by_id(account_id):
    logging.info('Request:{} \n\n Response: {}'.format(account_id, Account.__dict__))
    return Account.query.filter(Account.id == account_id).first()


@blueprint.route('/api/accounts', methods=['GET'])
@check_token
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int(), 'search': fields.Str()}, location="query")
@marshal_with(account_schemas)
def get_accounts(search, limit=20, offset=0):
    if search is not None:
        search_string = "%{}%".format(search)
        return Account.query.filter(or_(Account.email.like(search_string), Account.phone_number.like(search_string))). \
            offset(offset).limit(limit).all()

    return Account.query.offset(offset).limit(limit).all()


@blueprint.route('/api/account', methods=['PUT'])
@check_token
@use_kwargs(account_schema)
@marshal_with(account_schema)
def update_account(**kwargs):
    account = request.account
    kwargs.pop('email', None)
    # kwargs.pop('email', None)
    kwargs.pop('created_at', None)
    # todo fix updated_at on updates
    kwargs.pop('updated_at', None)
    # send welcome email to new account
    if not account.first_name:
        email_data = {
            "transactional_message_id": 15,
            "to": account.email,
            "identifiers": {"id": account.id},
            "message_data": {
                "fname": kwargs.get('first_name', 'Buddy')
            }
        }
        send_mail(email_data)
    account.update(**kwargs)
    account.verification_stage = get_account_verification_stage(account)

    return account


# For Development purposes. Api route to sign up a new user
@blueprint.route('/api/account/signup', methods=['POST'])
@use_kwargs({'email': fields.Str()})
@marshal_with(account_schema)
def signup(email):
    
    try:
        #if account doesin't exist, create account with 4 digit unique code
        account = Account.query.filter(Account.email == email).first()
        if not account:
            account = Account(email=email, code=random.randint(1000, 9999), kyc_level="KYC_LEVEL_0", registered_through="Internal")
            account.save()
            return jsonify({"message": "{} created successfully".format(account.email), "status_code": 201})
        else:
            print("Account already exists")
            return jsonify({"error": "Account already exists"})
        
    except Exception as e:
        return jsonify({"message": str(e)})




#complete verify email is code is correct
@blueprint.route('/api/account/verify', methods=['POST'])
@marshal_with(account_schema)
@use_kwargs({'code': fields.Str()})
def verify_email(code):
    account = Account.query.filter(Account.code == code).first()
    if account:
        account.kyc_level = "KYC_LEVEL_1"
        account.save()
        return account
    elif not account:
        return jsonify({"error": "Account not found"})
        # return jsonify({"message": account})
    else:
        return jsonify({"error": "Wrong Code"})



#complete account profile information
@blueprint.route('/api/account/complete-signup', methods=['POST'])
@marshal_with(account_schema)
@use_kwargs({'first_name': fields.Str(), 'last_name': fields.Str(),'role_id': fields.Int(), 'password': fields.Str(), 'account_id': fields.Int()})
def complete_profile(first_name,last_name,role_id,password,account_id):
    try:
        account = Account.query.filter(Account.id == account_id).first()
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        #update account with new password
        account.update(first_name=first_name, last_name=last_name, password=pw_hash, role_id=role_id)
        account.kyc_level = "KYC_LEVEL_2"
        # token = jwt.encode({'email': account.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, 'secret', algorithm='HS256')
        return account
        # return {"message": account, "token": token.decode('utf-8'), "status_code": 201}  
    except Exception as e:
        return jsonify({"error": str(e)})


#Create roles
@blueprint.route('/api/role', methods=['POST'])
@marshal_with(role_schema)
@use_kwargs({'name': fields.Str()})
def create_role(name):
    try:
        role = Role.create(name=name)
        return Response(json.dumps({'message': role.name}), status=201, mimetype='application/json')
    except Exception as e:
        return {'message': str(e)}, 400


#Get roles
@blueprint.route('/api/allroles', methods=['GET'])
@marshal_with(role_schemas)
def get_all_roles():
    try:
        roles = Role.query.all()
        return roles
    except Exception as e:
        return {'message': str(e)}, 400
    


#Create login route with email and password
@blueprint.route('/api/account/login', methods=['POST'])
@use_kwargs({'email': fields.Str(), 'password': fields.Str()})
def login(email, password):
    try:
        account = Account.query.filter(Account.email == email).first()
        if account:
            if bcrypt.check_password_hash(account.password, password):
                token = jwt.encode({'email': account.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, 'secret', algorithm='HS256')
                return {"token": token.decode('utf-8'), "status_code": 200}
            else:
                return {"error": "Wrong Password"}
        else:
            return {"error": "Account not found"}
    except Exception as e:
        return {'message': str(e)}, 400


# For Development purposes. Api route to get a new token for a valid user
@blueprint.route('/api/account/token', methods=['POST'])
@use_kwargs({'email': fields.Str(), 'password': fields.Str()})
def token(email, password):
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        # logging.info('Request:{} \n\n Response: {}'.format(user, jwt) )
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'}, 400