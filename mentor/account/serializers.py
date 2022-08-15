# coding: utf-8

from email.policy import default
from marshmallow import Schema, fields, pre_load, post_dump


class AccountSchema(Schema):
    id = fields.Integer()
    email = fields.Email(default=None)
    password = fields.String(default=None)
    kyc_level = fields.String(default="KYC_LEVEL_0")
    # role_id = fields.Integer(default=None)
    registered_through = fields.String(default=None)
    code = fields.String(default=None)
    first_name = fields.Str()
    last_name = fields.Str()
    createdAt = fields.DateTime(attribute="created_at", dump_only=True)
    updatedAt = fields.DateTime(attribute="updated_at")
    role = fields.Nested(
        "RoleSchema", only=("id", "name", "description"), dump_only=True
    )
    expertise = fields.Nested(
        "ExpertiseSchema", many=True, dump_only=True
    )

    workexperience_schema = fields.Nested(
        "WorkExperienceSchema", many=True, dump_only=True
    )
    # booking = fields.Nested("BookingSchema", dump_only=True)
    # slot = fields.Nested("SlotSchema", dump_only=True)



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
    country = fields.String()
    date_of_birth = fields.Date()
    gender = fields.String()
    language = fields.String()
    marital_status = fields.String()
    education = fields.String()
    account_id = fields.Integer()
    account = fields.Nested(
        "AccountSchema",dump_only=True
    )
    expertises = fields.Nested(
        "AccountExpertiseSchema", many=True
    )
    work_experiences = fields.Nested(
        "AccountWorkExperienceSchema", many=True
    )
    educations = fields.Nested(
        "AccountEducationSchema", many=True
    )
    social_medias = fields.Nested(
        "AccountSocialMediaSchema", many=True
    )

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
class ExpertiseSchema(Schema):
    id = fields.Integer()
    name = fields.String()

    @pre_load
    def make_expertise(self, data, **kwargs):
        return data

    @post_dump
    def dump_expertise(self, data, **kwargs):
        return data

    class Meta:
        strict = True

expertise_schema = ExpertiseSchema()
expertise_schemas = ExpertiseSchema(many=True)

class AccountExpertiseSchema(Schema):
    expertise = fields.Nested(
        "ExpertiseSchema",dump_only=True
    )

    @pre_load
    def make_account_expertise(self, data, **kwargs):
        return data

    @post_dump
    def dump_account_expertise(self, data, **kwargs):
        return data

    class Meta:
        strict = True

accountexpertise_schema = AccountExpertiseSchema()
accountexpertise_schemas = AccountExpertiseSchema(many=True)

class WorkExperienceSchema(Schema):
    id = fields.Integer()
    company_name = fields.String()
    position = fields.String()
    start_date = fields.Date()
    end_date = fields.Date()
    description = fields.String()

    @pre_load
    def make_workexperience(self, data, **kwargs):
        return data

    @post_dump
    def dump_workexperience(self, data, **kwargs):
        return data

    class Meta:
        strict = True

workexperience_schema = WorkExperienceSchema()
workexperience_schemas = WorkExperienceSchema(many=True)


class AccountWorkExperienceSchema(Schema):
    work_experience = fields.Nested(
        "WorkExperienceSchema",dump_only=True
    )

    @pre_load
    def make_account_work_experience(self, data, **kwargs):
        return data

    @post_dump
    def dump_account_work_experience(self, data, **kwargs):
        return data

    class Meta:
        strict = True

accountworkexperience_schema = AccountWorkExperienceSchema()
accountworkexperience_schemas = AccountWorkExperienceSchema(many=True)


class EducationSchema(Schema):
    id = fields.Integer()
    institution_name = fields.String()
    course = fields.String()
    start_date = fields.Date()
    end_date = fields.Date()
    description = fields.String()

    @pre_load
    def make_education(self, data, **kwargs):
        return data

    @post_dump
    def dump_education(self, data, **kwargs):
        return data

    class Meta:
        strict = True

education_schema = EducationSchema()
education_schemas = EducationSchema(many=True)


class SocialMediaSchema(Schema):
    id = fields.Integer()
    social_media_type = fields.String()
    social_media_link = fields.String()

    @pre_load
    def make_socialmedia(self, data, **kwargs):
        return data

    @post_dump
    def dump_socialmedia(self, data, **kwargs):
        return data

    class Meta:
        strict = True

socialmedia_schema = SocialMediaSchema()
socialmedia_schemas = SocialMediaSchema(many=True)






class AccountEducationSchema(Schema):
    education = fields.Nested(
        "EducationSchema",dump_only=True
    )

    @pre_load
    def make_account_education(self, data, **kwargs):
        return data

    @post_dump
    def dump_account_education(self, data, **kwargs):
        return data

    class Meta:
        strict = True


accounteducation_schema = AccountEducationSchema()
accounteducation_schemas = AccountEducationSchema(many=True)


class AccountSocialMediaSchema(Schema):
    social_media = fields.Nested(
        "SocialMediaSchema",dump_only=True
    )

    @pre_load
    def make_account_social_media(self, data, **kwargs):
        return data

    @post_dump
    def dump_account_social_media(self, data, **kwargs):
        return data

    class Meta:
        strict = True


accountsocialmedia_schema = AccountSocialMediaSchema()
accountsocialmedia_schemas = AccountSocialMediaSchema(many=True)

