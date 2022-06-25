# -*- coding: utf-8 -*-
"""Booking models."""
import datetime as dt

from sqlalchemy import ForeignKey

from mentor.database import Column, Model, SurrogatePK, db, relationship


class Booking(SurrogatePK, Model):
    __tablename__ = 'booking'

    mentee_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
    mentee = relationship('Account', back_populates='bookings')
    mentor_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
    mentor = relationship('Account', back_populates='bookings')
    start_time = Column(db.DateTime, nullable=False)
    end_time = Column(db.DateTime, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, mentee_id, mentor_id, start_time, end_time, **kwargs):
        """Create instance."""
        db.Model.__init__(self, mentee_id=mentee_id, mentor_id=mentor_id, start_time=start_time, end_time=end_time, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Booking({account_id!r})>'.format(mentee_id=self.mentee_id)

    def get_booking(self):
        return self.mentee_id