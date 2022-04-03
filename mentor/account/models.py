# -*- coding: utf-8 -*-
"""Account models."""
import datetime as dt

from sqlalchemy import ForeignKey

from mentor.database import Column, Model, SurrogatePK, db, relationship


class Account(SurrogatePK, Model):
    __tablename__ = 'account'
    
    first_name = Column(db.String(100), nullable=True)
    last_name = Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = Column(db.String(100), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    
    

    def __init__(self, email, **kwargs):
        """Create instance."""
        db.Model.__init__(self, email=email, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({email!r})>'.format(email=self.email)


    def get_account(self):
        return self.first_name