# -*- coding: utf-8 -*-
"""Account models."""
import datetime as dt

from sqlalchemy import ForeignKey

from mentor.database import Column, Model, SurrogatePK, db, relationship


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

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "kyc_level": self.kyc_level,
            "role_id": self.role_id,
            "registered_through": self.registered_through,
            "code": self.code,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

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
    date_of_birth = Column(db.Date)
    gender = Column(db.Enum("male", "female", "other", name="varchar"))
    marital_status = Column(
        db.Enum("single", "married", "divorced", "widowed", name="varchar")
    )
    education = Column(
        db.Enum("undergraduate", "graduate", "post_graduate", name="varchar")
    )
    country = Column(db.Text())
    language = Column(db.Text())
    account_id = Column(
        db.Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        unique=True,
        index=True,
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
