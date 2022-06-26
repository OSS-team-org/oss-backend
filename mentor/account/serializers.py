# coding: utf-8

from email.policy import default
from marshmallow import Schema, fields, pre_load, post_dump


class AccountSchema(Schema):
    id = fields.Integer()
    email = fields.Email(default=None)
    password = fields.String(default=None)
    kyc_level = fields.String(default="KYC_LEVEL_0")
    role_id = fields.Integer(default=None)
    registered_through = fields.String(default=None)
    code = fields.String(default=None)
    first_name = fields.Str()
    last_name = fields.Str()
    createdAt = fields.DateTime(attribute="created_at", dump_only=True)
    updatedAt = fields.DateTime(attribute="updated_at")
    role = fields.Nested(
        "RoleSchema", only=("id", "name", "description"), dump_only=True
    )

    @pre_load
    def make_account(self, data, **kwargs):
        return data

    @post_dump
    def dump_account(self, data, **kwargs):
        return data

    class Meta:
        strict = True


account_schema = AccountSchema()
account_schemas = AccountSchema(many=True)


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()

    @pre_load
    def make_role(self, data, **kwargs):
        return data

    @post_dump
    def dump_role(self, data, **kwargs):
        return data

    class Meta:
        strict = True


role_schema = RoleSchema()
role_schemas = RoleSchema(many=True)


class AccountprofileSchema(Schema):
    id = fields.Integer()
    profile_picture = fields.String()
    bio = fields.String()
    date_of_birth = fields.Date()
    country = fields.String()
    language = fields.String()
    expertise = fields.String()

    @pre_load
    def make_userprofile(self, data, **kwargs):
        return data

    @post_dump
    def dump_userprofile(self, data, **kwargs):
        return data

    class Meta:
        strict = True


accountprofile_schema = AccountprofileSchema()
accountprofile_schemas = AccountprofileSchema(many=True)
