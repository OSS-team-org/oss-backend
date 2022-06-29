# -*- coding: utf-8 -*-
"""Account models."""
import datetime as dt

from sqlalchemy import ForeignKey

from mentor.database import Column, Model, SurrogatePK, db, relationship

#account model
class Account(SurrogatePK, Model):
    __tablename__ = "account"

    first_name = Column(db.String(100), nullable=True)
    last_name = Column(db.String(100), nullable=True)
    kyc_level = Column(db.String(100), nullable=False)
    role_id = Column(db.Integer, ForeignKey("role.id"), nullable=True)
    expertise = relationship("Expertise", secondary="account_expertise", backref="accounts")
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
    country = Column(db.Text())
    language = Column(db.Text())
    account_id = Column(
        db.Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        unique=True,
    )
    account = relationship(
        "Account", back_populates="account_profile", single_parent=True
    )

    def __init__(self, bio, **kwargs):
        """Create instance."""
        db.Model.__init__(self, bio=bio, **kwargs)

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
    account_id = Column(
        db.Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        unique=True,
    )
    account = relationship(
        "Account", back_populates="work_experience", single_parent=True
    )

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

    insitution_name = Column(db.String(100), nullable=True)
    course = Column(db.String(100), nullable=True)
    start_date = Column(db.Date, nullable=True)
    end_date = Column(db.Date, nullable=True)
    description = Column(db.Text(), nullable=True)
    account_id = Column(
        db.Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        unique=True,
    )
    account = relationship(
        "Account", back_populates="education", single_parent=True
    )

    def __init__(self, school_name, start_date, end_date, description, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self,
            school_name=school_name,
            start_date=start_date,
            end_date=end_date,
            description=description,
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Education({school_name!r})>".format(school_name=self.school_name)

class SocialMedia(SurrogatePK, Model):
    __tablename__ = "social_media"

    social_media_name = Column(db.String(100), nullable=True)
    social_media_link = Column(db.String(100), nullable=True)
    account_id = Column(
        db.Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        unique=True,
    )
    account = relationship(
        "Account", back_populates="social_media", single_parent=True
    )

    def __init__(self, social_media_name, social_media_link, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self,
            social_media_name=social_media_name,
            social_media_link=social_media_link,
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<SocialMedia({social_media_name!r})>".format(social_media_name=self.social_media_name)


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
    def __init__(self, name):
        """Create instance."""
        db.Model.__init__(self, name=name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Expertise({name!r})>".format(name=self.name)


account_expertise = db.Table(
    "account_expertise",
    db.Column("account_id", db.Integer, ForeignKey("account.id")),
    db.Column("expertise_id", db.Integer, ForeignKey("expertise.id")),
)