# -*- coding: utf-8 -*-
"""Booking models."""
import datetime as dt

from sqlalchemy import ForeignKey

from mentor.database import Column, Model, SurrogatePK, db, relationship


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


# tags = db.Table('servicetag',
#     db.Column('servicetag_id', db.Integer, ForeignKey('servicetag.id')),
#     db.Column('booking_id', db.Integer, ForeignKey('booking.id'))
# )

class Booking(SurrogatePK, Model):
    __tablename__ = 'booking'

    mentee_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
    mentee = relationship('Account', back_populates='booking')
    slot_id = Column(db.Integer, ForeignKey('slot.id'), nullable=False)
    slot = relationship('Slot', back_populates='booking')
    tags = relationship('TagAccount', back_populates='booking')
    description = Column(db.Text, nullable=True)
    status = Column(db.String(50), nullable=False)
    is_confirmed = Column(db.Boolean, default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, mentee_id, slot_id, tags, description, status, is_confirmed, created_at, updated_at, **kwargs):
        """Create instance"""
        db.Model.__init__(
            self,
            mentee_id=mentee_id,
            slot_id=slot_id,
            tags=tags,
            description=description,
            status=status,
            is_confirmed=is_confirmed,
            created_at=created_at,
            updated_at=updated_at,
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return 'Booking(' + str(self.mentee_id) + ',' + str(self.slot_id) + ')'


class Slot(SurrogatePK, Model):
    __tablename__ = 'slot'

    mentor_id = Column(db.Integer, ForeignKey('account.id'), nullable=False)
    mentor = relationship('Account', back_populates='slot')
    weekday_id = Column(db.Integer, ForeignKey('weekday.id'), nullable=False)
    weekday = relationship('WeekDay', back_populates='slot')
    start_time = Column(db.DateTime, nullable=False)
    duration = Column(db.Integer, nullable=False)
# end_time auto calculated
    end_time = Column(db.DateTime, nullable=True)
    is_booked = Column(db.Boolean, default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    booking = relationship('Booking', back_populates='slot')

    def __init__(self, mentor_id, weekday_id, start_time, duration, end_time, is_booked, created_at, updated_at, **kwargs):
        """Create instance"""
        db.Model.__init__(
            self,
            mentor_id=mentor_id,
            weekday_id=weekday_id,
            start_time=start_time,
            duration=duration,
            end_time=end_time,
            is_booked=is_booked,
            created_at=created_at,
            updated_at=updated_at,
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return 'Slot(' + str(self.mentor_id) + ',' + str(self.start_time) + "-" + str(self.end_time) + ')'
        # return 'Slot(' + str(self.mentor_id) + ',' + str(self.start_time) + ')'


class Tag(SurrogatePK, Model):
    __tablename__ = 'tag'

    name = Column(db.String(100), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    bookings = relationship('TagAccount', back_populates='tag')

    def __init__(self, name, created_at, updated_at):
        """Create instance"""
        db.Model.__init__(self, name=name, created_at=created_at, updated_at=updated_at)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Tag %r>' % self.name


class TagAccount(SurrogatePK, Model):
    __tablename__ = 'tag_account'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = Column(db.Integer, ForeignKey('booking.id'), nullable=False, primary_key=True)
    booking = relationship('Booking', back_populates='tags')
    tag_id = Column(db.Integer, ForeignKey('tag.id'), nullable=False, primary_key=True)
    tag = relationship('Tag', back_populates='bookings')

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<TagAccount({booking_id!r}, {tag_id!r})>".format(
            booking_id=self.booking_id, tag_id=self.tag_id
        )


class WeekDay(SurrogatePK, Model):
    __tablename__ = 'weekday'

    name = Column(db.String(100), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    slot = relationship('Slot', back_populates='weekday')

    def __init__(self, name, created_at, updated_at, **kwargs):
        """Create instance"""
        db.Model.__init__(self, name=name, created_at=created_at, updated_at=updated_at,  **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<WeekDay %r>' % self.name
