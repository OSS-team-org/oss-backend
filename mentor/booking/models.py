# -*- coding: utf-8 -*-
"""Booking models."""
import datetime as dt
from xmlrpc.client import DateTime

from sqlalchemy import ForeignKey

from mentor.database import Column, Model, SurrogatePK, db, relationship


# class Booking(SurrogatePK, Model):
#     __tablename__ = 'booking'

#     mentee_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
#     mentee = relationship('Account', back_populates='bookings')
#     mentor_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
#     mentor = relationship('Account', back_populates='bookings')
#     start_time = Column(db.DateTime, nullable=False)
#     end_time = Column(db.DateTime, nullable=False)
#     created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
#     updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

#     def __init__(self, mentee_id, mentor_id, start_time, end_time, **kwargs):
#         """Create instance."""
#         db.Model.__init__(self, mentee_id=mentee_id, mentor_id=mentor_id, start_time=start_time, end_time=end_time, **kwargs)

#     def __repr__(self):
#         """Represent instance as a unique string."""
#         return '<Booking({account_id!r})>'.format(mentee_id=self.mentee_id)

#     def get_booking(self):
#         return self.mentee_id

"""
Booking Flow:
1. Mentors create times they're available within the day.
    Eg. Monday `10:00:00-10:30:00`, `11:30:00-14:00:00`, `15:00:00-17:00:00` etc
        Thursday `9:00:00-10:30:00`, `13:00:00-14:00:00`, `15:00:00-17:00:00` etc
    
2. Mentee selects the following when booking
    i.  slot from the list of slots available
    ii. tags eg. `career growth`, `career_advice`, `women_empowerment` etc
    iii. description of what they need etc
    iv. create booking
"""


tags = db.Table('servicetag',
        db.Column('servicetag_id', db.Integer, ForeignKey('servicetag.id')),
        db.Column('booking_id', db.Integer, ForeignKey('booking.id'))
)

class Booking(SurrogatePK, Model):
    __tablename__ = 'booking'

    mentee_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
    mentee = relationship('Account', back_populates='bookings')
    slot_id = Column(db.Integer, ForeignKey('slot.id'), nullable=False)
    slot = relationship('TimeSlot', backpopulates='bookings', order_by='TimeSlot.id')
    tag_id = Column(db.Integer, ForeignKey('servicetag.id'), nullable=True)
    # tags = relationship('ServiceTag', backpopulates='bookings', order_by='ServiceTag.id')
    tags = relationship(
        'ServiceTag',
        secondary=tags,
        lazy='subquery',
        backref=db.backref('bookings', lazy=True)
    )
    description = Column(db.Text, nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, mentee_id, slot, servicetag_id, **kwargs):
        """Create instance"""
        db.Model.__init__(self, mentee_id=mentee_id, slot=slot, servicetag_id=servicetag_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return 'Booking(' + str(self.mentee_id) + ',' + str(self.slot_id) + ')'


class TimeSlot(SurrogatePK, Model):
    __tablename__ = 'timeslot'

    mentor_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
    mentor = relationship('Account', back_populates='timeslots')
    weekday_id = Column(db.Integer, ForeignKey('weekday.id'), nullable=False)
    weekday = relationship('WeekDay', back_populates='timeslots')
    start_time = Column(db.DateTime, nullable=False)
    duration = Column(db.Integer, nullable=False)
# end_time auto calculated
    # end_time = Column(db.DateTime, nullable=True)
    is_booked = Column(db.Boolean, default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, mentor_id, weekday_id, start_time, duration, end_time, **kwargs):
        """Create instance"""
        db.Model.__init__(self, mentor_id=mentor_id, weekday_id=weekday_id, start_time=start_time, duration=duration, end_time=end_time, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        # return 'TimeSlot(' + str(self.mentor_id) + ',' + str(self.start_time) + "-" + str(self.end_time) + ')'
        return 'TimeSlot(' + str(self.mentor_id) + ',' + str(self.start_time) + ')'


class ServiceTag(SurrogatePK, Model):
    __tablename__ = 'servicetag'

    name = Column(db.String(100), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, name, **kwargs):
        """Create instance"""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<ServiceTag %r>' % self.name


class WeekDay(SurrogatePK, Model):
    __tablename__ = 'weekday'

    name = Column(db.String(100), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, name, **kwargs):
        """Create instance"""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<WeekDay %r>' % self.name