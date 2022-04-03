# coding: utf-8

from email.policy import default
from marshmallow import Schema, fields, pre_load, post_dump


class AccountSchema(Schema):
    id = fields.Integer()
    email = fields.Email(default=None)
    password = fields.String(default=None)
    first_name = fields.Str()
    last_name = fields.Str()
    createdAt = fields.DateTime(attribute='created_at', dump_only=True)
    updatedAt = fields.DateTime(attribute='updated_at')

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