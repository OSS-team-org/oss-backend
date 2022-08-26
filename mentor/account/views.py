# -*- coding: utf-8 -*-
"""User views."""
import logging
import json
import random
import os
import requests

# push
# from firebase_admin import auth
from flask import (
    Blueprint,
    request,
    Response,
    jsonify,
    redirect,
    url_for,
    render_template,
    session,
)
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields
from sqlalchemy import null, or_
import datetime
import jwt
from flask_bcrypt import Bcrypt
from .models import Account, Role, UserRoles, Accountprofile, Expertise, WorkExperience, Education, SocialMedia, ExpertiseAccount, Account_Workexperience, Account_Education, Account_SocialMedia, SocialMedia
from flask_github import GitHub
from flask_restx import Api, Resource

from .serializers import (
    account_schema,
    account_schemas,
    role_schema,
    role_schemas,
    accountprofile_schema,
    accountprofile_schemas,
    expertise_schema,
    expertise_schemas,
    accountexpertise_schema,
    workexperience_schema,
    workexperience_schemas,
    education_schema,
    education_schemas,
    socialmedia_schema,
    accountsocialmedia_schema,
    accountsocialmedia_schemas,
    accountexpertise_schema,
    accountexpertise_schemas,
    AccountprofileSchema
)

# from ..firebase import pb
from mentor.middleware import check_token

# import WebapplicationClient from oauth2client.oauth2
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_mail import Mail
from flask_mail import Message

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
# from ..utils import get_account_verification_stage, send_mail

blueprint = Blueprint("account", __name__)
bcrypt = Bcrypt()
mail = Mail()
api = Api()
client = WebApplicationClient(GOOGLE_CLIENT_ID)
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized
# from flask_restplus import Namespace, Resource, fields


github_blueprint = make_github_blueprint(client_id = GOOGLE_CLIENT_ID, client_secret = GOOGLE_CLIENT_SECRET)
# namespace = Namespace('account', description='Account related operations')


@blueprint.route("/api/hello")
def hello_world():
    return "Hello World!"


@blueprint.route("/api/accounts/<int:account_id>", methods=["GET"])
@check_token
@marshal_with(account_schema)
def get_account_by_id(account_id):
    try:
        logging.info("Request:{} \n\n Response: {}".format(account_id, Account.__dict__))
        return Account.query.filter(Account.id == account_id).first()
    except Exception as e:
        logging.error(e)
        return {"message": "Error"}, 500


@blueprint.route("/api/accounts", methods=["GET"])
@check_token
@use_kwargs(
    {"limit": fields.Int(), "offset": fields.Int(), "search": fields.Str()},
    location="query",
)
@marshal_with(account_schemas)
def get_accounts(search, limit=20, offset=0):
    if search is not None:
        search_string = "%{}%".format(search)
        return (
            Account.query.filter(
                or_(
                    Account.email.like(search_string),
                    Account.phone_number.like(search_string),
                )
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    return Account.query.offset(offset).limit(limit).all()


# @blueprint.route('/api/account', methods=['PUT'])
# @check_token
# @use_kwargs(account_schema)
# @marshal_with(account_schema)
# def update_account(**kwargs):
#     account = request.account
#     kwargs.pop('email', None)
#     # kwargs.pop('email', None)
#     kwargs.pop('created_at', None)
#     # todo fix updated_at on updates
#     kwargs.pop('updated_at', None)
#     # send welcome email to new account
#     if not account.first_name:
#         email_data = {
#             "transactional_message_id": 15,
#             "to": account.email,
#             "identifiers": {"id": account.id},
#             "message_data": {
#                 "fname": kwargs.get('first_name', 'Buddy')
#             }
#         }
#         send_mail(email_data)
#     account.update(**kwargs)
#     account.verification_stage = get_account_verification_stage(account)

#     return account


# For Development purposes. Api route to sign up a new user
@blueprint.route("/api/account/signup", methods=["POST"])
@use_kwargs({"email": fields.Str()})
@marshal_with(account_schema)
def signup(email):

    try:
        # if account doesin't exist, create account with 4 digit unique code
        account = Account.query.filter(Account.email == email).first()
        if not account:
            account = Account(
                email=email,
                code=random.randint(1000, 9999),
                kyc_level="KYC_LEVEL_0",
                registered_through="Internal",
            )
            # send code with flask mail
            msg = Message(
                "Mentor Connect", sender=MAIL_USERNAME, recipients=[account.email]
            )
            account.save()
            msg.body = "Please enter the code %s to verify your email address" % (account.code)
            mail.send(msg)
            return jsonify(
                {
                    "message": "{} created successfully".format(account.email),
                    "status_code": 201,
                }
            )
        else:
            return jsonify({"error": "Account already exists"})
    except Exception as e:
        return jsonify({"message": str(e)})


# complete verify email is code is correct
@blueprint.route("/api/account/verify", methods=["POST"])
@marshal_with(account_schema)
@use_kwargs({"code": fields.Str()})
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


# complete account profile information
@blueprint.route("/api/account/complete-signup", methods=["POST"])
@marshal_with(account_schema)
@use_kwargs(
    {
        "first_name": fields.Str(),
        "last_name": fields.Str(),
        "role_id": fields.Int(),
        "password": fields.Str(),
        "account_id": fields.Int(),
    }
)
def complete_profile(first_name, last_name, role_id, password, account_id):
    try:
        account = Account.query.filter(Account.id == account_id).first()
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        # update account with new password
        account.update(
            first_name=first_name,
            last_name=last_name,
            password=pw_hash,
            role_id=role_id,
        )
        account.kyc_level = "KYC_LEVEL_2"
        # token = jwt.encode({'email': account.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, 'secret', algorithm='HS256')
        return account
        # return {"message": account, "token": token.decode('utf-8'), "status_code": 201}
    except Exception as e:
        return jsonify({"error": str(e)})


# Create roles
@blueprint.route("/api/role", methods=["POST"])
@marshal_with(role_schema)
@use_kwargs({"name": fields.Str()})
def create_role(name):
    try:
        role = Role.create(name=name)
        return Response(
            json.dumps({"response": role.name + " successfully created"}), status=201, mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


# Get roles
@blueprint.route("/api/allroles", methods=["GET"])
@marshal_with(role_schemas)
def get_all_roles():
    try:
        roles = Role.query.all()
        return roles
    except Exception as e:
        return {"message": str(e)}, 400


# Create account profile
@blueprint.route("/api/account-profile", methods=["POST"])
@check_token
@use_kwargs(
    {
        "profile_picture": fields.Str(),
        "country": fields.Str(),
        "language": fields.Str(),
        "bio": fields.Str(),
        "account_id": fields.Int(),
        "education": fields.Str(),
        "gender": fields.Str(),
        "marital_status": fields.Str(),
        "date_of_birth": fields.Date(),
        "expertise_ids": fields.List(fields.Int())
    }
)
def create_account_profile(
    profile_picture, country, language, bio, account_id, education, gender, marital_status, date_of_birth, expertise_ids=None
):

    try:
        account_profile = Accountprofile(
            profile_picture=profile_picture,
            country=country,
            language=language,
            bio=bio,
            account_id=account_id,
            education=education,
            gender=gender,
            marital_status=marital_status,
            date_of_birth=date_of_birth
        )
        account_profile.save()

        #unpack expertise_ids array and store in ExpertiseAccount
        for expertise_id in expertise_ids:
            expertise_account = ExpertiseAccount(
                account_id=account_profile.id,
                expertise_id=expertise_id
            )
            expertise_account.save()
            #return expertise and account_profile
        # print(AccountprofileSchema().dump(Accountprofile.query.get(account_profile.id)))
        #return account profile and expertise data
        return AccountprofileSchema().dump(Accountprofile.query.get(account_profile.id))
    except Exception as e:
        # print(str(e))
        return {"message": str(e)}, 400


# @blueprint.route("/api/account-expertise", methods=["POST"])
# @use_kwargs(
#     {
#         "account_id": fields.Int(),
#         "expertise_ids": fields.List(fields.Int())
#     }
# )
# @marshal_with(accountexpertise_schema)
# def create_expertise_account(account_id, expertise_ids):
#     try:
#         for expertise_id in expertise_ids:
#             expertise_account = ExpertiseAccount(
#                 account_id=account_id,
#                 expertise_id=expertise_id
#             )
#             expertise_account.save()
            
#     except Exception as e:
#         print(str(e))
#         return {"message": str(e)}, 400


#Create account work experience
@blueprint.route("/api/account-work-experience", methods=["POST"])
# @marshal_with(workexperience_schema)
@check_token
@use_kwargs(
    {
        "company_name": fields.Str(),
        "position": fields.Str(),
        "start_date": fields.Date(),
        "end_date": fields.Date(),
        "account_profileid": fields.Int(),
        "description": fields.Str(),
    }
)
def create_account_work_experience(
    company_name,
    position,
    start_date,
    end_date,
    account_profileid,
    description
):
    try:
        work_experience = WorkExperience(
            company_name=company_name,
            position=position,
            start_date=start_date,
            end_date=end_date,
            description=description
        ) 
        work_experience.save()

        account_workexperience=Account_Workexperience(
            account_id=account_profileid,
            work_experience_id=work_experience.id
        )

        account_workexperience.save()
        
        # print(AccountprofileSchema().dump(Accountprofile.query.get(account_profileid)))
        return AccountprofileSchema().dump(Accountprofile.query.get(account_profileid))
    except Exception as e:
        # print(e)
        return {"message": str(e)}, 400


#Delete account work experience
@blueprint.route("/api/account-work-experience/<id>", methods=["DELETE"])
@check_token
def delete_account_work_experience(id):
    try:
        work_experience = WorkExperience.query.get(id)
        work_experience.delete()
        return {"message": "Work experience successfully deleted"}
    except Exception as e:
        return {"message": str(e)}, 400

#creating a new branch
#creating a new branch
#Create account education
@blueprint.route("/api/account-education", methods=["POST"])
# @marshal_with(education_schema)
@check_token
@use_kwargs(
    {
        "institution_name": fields.Str(),
        "start_date": fields.Date(),
        "end_date": fields.Date(),
        "account_profileid": fields.Int(),
        "description": fields.Str(),
    }
)
def create_account_education(
    institution_name,
    start_date,
    end_date,
    account_profileid,
    description
):
    try:
        education = Education(
            institution_name=institution_name,
            start_date=start_date,
            end_date=end_date,
            description=description
        ) 
        education.save()

        account_education=Account_Education(
            account_id=account_profileid,
            education_id=education.id
        )

        account_education.save()
        

        
        # print(AccountprofileSchema().dump(Accountprofile.query.get(account_profileid)))
        return AccountprofileSchema().dump(Accountprofile.query.get(account_profileid))
    except Exception as e:
        # print(e)
        return {"message": str(e)}, 400


#Create social media
@blueprint.route("/api/account-social-media", methods=["POST"])
# @marshal_with(socialmedia_schema)
@check_token
@use_kwargs(
    {
        "social_media_type": fields.Str(),
        "social_media_link": fields.Str(),
        "account_profileid": fields.Int(),
    }
)
def create_account_social_media(account_profileid, social_media_type, social_media_link):
    try:
        social_media = SocialMedia(
            social_media_type=social_media_type,
            social_media_link=social_media_link
        ) 
        social_media.save()

        account_socialmedia=Account_SocialMedia(
            account_id=account_profileid,
            social_media_id=social_media.id
        )

        account_socialmedia.save()
        

        
        # print(AccountprofileSchema().dump(Accountprofile.query.get(account_profileid)))
        return AccountprofileSchema().dump(Accountprofile.query.get(account_profileid))
    except Exception as e:
        # print(e)
        return {"message": str(e)}, 400



# Get account profiles
@blueprint.route("/api/allaccount_profiles", methods=["GET"])
@marshal_with(accountprofile_schemas)
@check_token
def get_all_account_profiles():
    try:
        account_profiles = Accountprofile.query.all()
        return account_profiles
    except Exception as e:
        return {"message": str(e)}, 400


# Create login route with email and password
@blueprint.route("/api/account/login", methods=["POST"])
@use_kwargs({"email": fields.Str(), "password": fields.Str()})
def login(email, password):
    try:
        account = Account.query.filter(Account.email == email).first()
        if account:
            if bcrypt.check_password_hash(account.password, password):
                token = jwt.encode(
                    {
                        "email": account.email,
                        "exp": datetime.datetime.utcnow()
                        + datetime.timedelta(minutes=50),
                    },
                    "secret",
                    algorithm="HS256",
                )
                return {"token": token.decode("utf-8"), "status_code": 200}
            else:
                return {"error": "Wrong Password"}
        else:
            return {"error": "Account not found"}
    except Exception as e:
        return {"message": str(e)}, 400


# get google provider configurations
@blueprint.route("/api/google-provider", methods=["GET"])
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@blueprint.route("/login", methods=["GET"])
def google_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return {"request_uri": request_uri}


@blueprint.route("/login/callback")
def google_callback():
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=request.args.get("code"),
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        # unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        first_name = userinfo_response.json()["given_name"]
        last_name = userinfo_response.json()["family_name"]
        # picture = userinfo_response.json()["picture"]
        # users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # print(userinfo_response.json())
    account = Account.query.filter(Account.email == users_email).first()
    if not account:
        account = Account(
            email=users_email,
            code=random.randint(1000, 9999),
            kyc_level="KYC_LEVEL_1",
            registered_through="Google",
            first_name=first_name,
            last_name=last_name,
        )
        account.save()
        return redirect(
            url_for(
                "account.complete_profile",
                role_id=2,
                password="",
                account_id=account.id,
            )
        )
    else:
        return redirect(url_for("account.login", email=users_email, password=""))


# # For Development purposes. Api route to get a new token for a valid user
# @blueprint.route('/api/account/token', methods=['POST'])
# @use_kwargs({'email': fields.Str(), 'password': fields.Str()})
# def token(email, password):
#     try:
#         user = pb.auth().sign_in_with_email_and_password(email, password)
#         jwt = user['idToken']
#         # logging.info('Request:{} \n\n Response: {}'.format(user, jwt) )
#         return {'token': jwt}, 200
#     except:
#         return {'message': 'There was an error logging in'}, 400


# @blueprint.route('/github_login/github/authorized', methods=['GET'])
# def authorized():
#     if request.args.get('code'):
#         # If there is a code, then it's a successful login
#         code = request.args.get('code')
#         # Get the access token
#         access_token = github.get_access_token(code)
#         # Get the user's information
#         user = github.get('user', access_token=access_token)
#         # Create a new account if it doesn't exist
#         return {'message': 'Successfully logged in as {}'.format(user['login'])}
#     else:
#         return {'message': 'No code returned'}


@oauth_authorized.connect_via(github_blueprint)
@blueprint.route("/githublogin")
def github_login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    else:
        account_info = github.get('/user') 
        if account_info.ok:
            if Account.query.filter(Account.email == account_info.json()['email']).first():
                return {'message': 'Account already exists'}, 400
            elif account_info.json()['email'] is null or account_info.json()['email'] is None:
                return {'message': 'Email not available'}, 400
            else:
                account = Account(email=account_info.json()['email'], code=random.randint(1000, 9999), kyc_level="KYC_LEVEL_1", registered_through="Github", first_name=account_info.json()['name'])
                account.save()
                return {'message': 'Successfully logged in as {}'.format(account_info.json()['login'])}

    return "<h1>Request failed!</h1>"


#create expertise endpoint
@blueprint.route("/api/expertise", methods=["POST"])
@use_kwargs({
    "name": fields.Str(required=True)
})
@marshal_with(expertise_schema)
def create_expertise(name):
    expertise = Expertise(name=name)
    expertise.save()
    return expertise, 201



#Get all expertise
@blueprint.route("/api/allexpertise", methods=["GET"])
@marshal_with(expertise_schema)
def get_all_expertise():
    return Expertise.query.all()




    
        
    
    






        
