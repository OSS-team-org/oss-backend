# -*- coding: utf-8 -*-
"""Account models."""
import datetime as dt
from enum import Enum
import enum

from sqlalchemy import ForeignKey

from mentor.database import Column, Model, SurrogatePK, db, relationship

#account model
class Account(SurrogatePK, Model):
    __tablename__ = "account"

    first_name = Column(db.String(100), nullable=True)
    last_name = Column(db.String(100), nullable=True)
    kyc_level = Column(db.String(100), nullable=False)
    role_id = Column(db.Integer, ForeignKey("role.id"), nullable=True)
    account_profile = relationship(
        "Accountprofile",
        uselist=False,
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="select",
    )
    
    
    role = relationship("Role", backref="accounts")
    email = db.Column(db.String(100), unique=True, nullable=False)
    registered_through = Column(db.String(100), nullable=True)
    password = Column(db.String(100), nullable=True)
    code = Column(db.String(100), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, email, **kwargs):
        """Create instance."""
        db.Model.__init__(self, email=email, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Account({email!r})>".format(email=self.email)

    def get_account(self):
        return self.first_name


class Role(SurrogatePK, Model):
    __tablename__ = "role"

    name = Column(db.String(80), unique=True, nullable=False)
    description = Column(db.String(255))

    def __init__(self, name, description=""):
        """Create instance."""
        db.Model.__init__(self, name=name, description=description)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Role({name!r})>".format(name=self.name)


class Accountprofile(SurrogatePK, Model):
    __tablename__ = "account_profile"

    profile_picture = Column(db.Text())
    bio = Column(db.Text())
    gender = Column(db.String(100), nullable=True)
    marital_status = Column(db.String(100), nullable=True)
    date_of_birth = Column(db.Date, nullable=True)
    education = Column(db.String(100), nullable=True)
    gender = Column(db.String)
    country = Column(db.Text())
    language = Column(db.Text())
    expertises = relationship("ExpertiseAccount", back_populates="account")
    work_experiences = relationship("Account_Workexperience", back_populates="account")
    educations = relationship("Account_Education", back_populates="account")
    social_medias = relationship("Account_SocialMedia", back_populates="soc_account")
    account_id = Column(
        db.Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        unique=True,
    )
    account = relationship(
        "Account", back_populates="account_profile", single_parent=True
    )

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self,**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Accountprofile({bio!r})>".format(bio=self.bio)


class WorkExperience(SurrogatePK, Model):
    __tablename__ = "work_experience"

    company_name = Column(db.String(100), nullable=True)
    position = Column(db.String(100), nullable=True)
    start_date = Column(db.Date, nullable=True)
    end_date = Column(db.Date, nullable=True)
    description = Column(db.Text(), nullable=True)
    accounts = relationship("Account_Workexperience", back_populates="work_experience")

    def __init__(self, company_name, position, start_date, end_date, description, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self,
            company_name=company_name,
            position=position,
            start_date=start_date,
            end_date=end_date,
            description=description,
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<WorkExperience({company_name!r})>".format(company_name=self.company_name)


class Education(SurrogatePK, Model):
    __tablename__ = "education"

    institution_name = Column(db.String(100), nullable=True)
    course = Column(db.String(100), nullable=True)
    start_date = Column(db.Date, nullable=True)
    end_date = Column(db.Date, nullable=True)
    description = Column(db.Text(), nullable=True)
    accounts = relationship("Account_Education", back_populates="education")
    

    def __init__(self, institution_name, start_date, end_date, description, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self,
            institution_name=institution_name,
            start_date=start_date,
            end_date=end_date,
            description=description,
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Education({institution_name!r})>".format(institution_name=self.institution_name)

class SocialMedia(SurrogatePK, Model):
    __tablename__ = "social_media"

    social_media_type = Column(db.String(100), nullable=True)
    social_media_link = Column(db.String(100), nullable=True)
    accounts = relationship("Account_SocialMedia", back_populates="social_media")

    def __init__(self, social_media_type, social_media_link, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self,
            social_media_type=social_media_type,
            social_media_link=social_media_link,
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<SocialMedia({social_media_type!r})>".format(social_media_type=self.social_media_type)


class UserRoles(SurrogatePK, Model):
    __tablename__ = "user_roles"

    account_id = Column(db.Integer, ForeignKey("account.id"), nullable=False)
    role_id = Column(db.Integer, ForeignKey("role.id"), nullable=False)

    account = relationship("Account", backref="user_roles")
    role = relationship("Role", backref="user_roles")

    def __init__(self, account_id, role_id):
        """Create instance."""
        db.Model.__init__(self, account_id=account_id, role_id=role_id)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<UserRoles({account_id!r}, {role_id!r})>".format(
            account_id=self.account_id, role_id=self.role_id
        )




class Expertise(SurrogatePK, Model):
    __tablename__ = "expertise"

    name = Column(db.String(100), nullable=False)

    accounts = relationship("ExpertiseAccount", back_populates="expertise")
    def __init__(self, name):
        """Create instance."""
        db.Model.__init__(self, name=name)

    def __repr__(self): 
        """Represent instance as a unique string."""
        return "<Expertise({name!r})>".format(name=self.name)


class ExpertiseAccount(Model):
    __tablename__ = "account_expertise"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = Column(db.Integer, ForeignKey("account_profile.id"), nullable=False, primary_key=True)
    expertise_id = Column(db.Integer, ForeignKey("expertise.id"), nullable=False, primary_key=True)

    account = relationship("Accountprofile", back_populates="expertises")
    expertise = relationship("Expertise", back_populates="accounts")

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<ExpertiseAccount({account_id!r}, {expertise_id!r})>".format(
            account_id=self.account_id, expertise_id=self.expertise_id
        )


class Account_Workexperience(Model):
    __tablename__ = "account_workexperience"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = Column(db.Integer, ForeignKey("account_profile.id"), nullable=False, primary_key=True)
    work_experience_id = Column(db.Integer, ForeignKey("work_experience.id"), nullable=False, primary_key=True)

    account = relationship("Accountprofile", back_populates="work_experiences")
    work_experience = relationship("WorkExperience", back_populates="accounts")

    def __init__(self, account_id, work_experience_id):
        """Create instance."""
        db.Model.__init__(self, account_id=account_id, work_experience_id=work_experience_id)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Account_Workexperience({account_id!r}, {work_experience_id!r})>".format(
            account_id=self.account_id, work_experience_id=self.work_experience_id
        )

#Association table for Education and Account
class Account_Education(Model):
    __tablename__ = "account_education"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = Column(db.Integer, ForeignKey("account_profile.id"), nullable=False, primary_key=True)
    education_id = Column(db.Integer, ForeignKey("education.id"), nullable=False, primary_key=True)

    account = relationship("Accountprofile", back_populates="educations")
    education = relationship("Education", back_populates="accounts")

    def __init__(self, account_id, education_id):
        """Create instance."""
        db.Model.__init__(self, account_id=account_id, education_id=education_id)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Account_Education({account_id!r}, {education_id!r})>".format(
            account_id=self.account_id, education_id=self.education_id
        )




class Account_SocialMedia(Model):
    __tablename__ = "account_socialmedia"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = Column(db.Integer, ForeignKey("account_profile.id"), nullable=False, primary_key=True)
    social_media_id = Column(db.Integer, ForeignKey("social_media.id"), nullable=False, primary_key=True)

    soc_account = relationship("Accountprofile", back_populates="social_medias")
    social_media = relationship("SocialMedia", back_populates="accounts")

    def __init__(self, account_id, social_media_id):
        """Create instance."""
        db.Model.__init__(self, account_id=account_id, social_media_id=social_media_id)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Account_SocialMedia({account_id!r}, {social_media_id!r})>".format(
            account_id=self.account_id, social_media_id=self.social_media_id
        )


