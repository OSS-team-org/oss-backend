from email.mime import application
import logging
import json
import mimetypes
import random
import os
import requests

from flask import Blueprint, Response
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields
from sqlalchemy import null, or_

from mentor.middleware import check_token

from .models import Booking, ServiceTag, Slot, WeekDay

from flask_restx import Api

from .serializers import (
    booking_schema,
    booking_schemas,
    slot_schema,
    slot_schemas,
    weekday_schema,
    weekday_schemas,
    servicetag_schema,
    servicetag_schemas
)

blueprint = Blueprint("booking", __name__)
api = Api()


# get all bookings
@blueprint.route("/api/bookings/bookings", methods=["GET"])
@check_token
@use_kwargs(
    {"limit": fields.Int(), "offset": fields.Int(), "search": fields.Str()},
    location="query",
)
@marshal_with(booking_schemas)
def get_bookings(search, limit=20, offset=0):
    if search is not None:
        search_string="%{}%".format(search)
        return(
            Booking.query.filter(
                or_(
                    Booking.created_at.like(search_string),
                    Booking.status.like(search_string),
                )
            )
            .offset(offset)
            .limit(limit)
            .all()
        )
    return Booking.query.offset(offset).limit(limit).all().order_by("created_at")


# get booking by id
@blueprint.route("/api/bookings/bookings/<int:booking_id>", methods=["GET"])
@check_token
@marshal_with(booking_schema)
def get_booking_by_id(booking_id):
    try:
        logging.info("Request:{} \n\n Response: {}".format(booking_id, Booking.__dict__))
        booking = Booking.query.filter(Booking.id==booking_id).first()
        return booking 
    except Exception as e:
        logging.error(e)
        return {"message": "Error"}, 500


# create booking
@blueprint.route("/api/bookings/booking", methods=["POST"])
@check_token
@marshal_with(booking_schema)
@use_kwargs({
    "mentee_id": fields.Int(),
    "slot_id": fields.Int(),
    "tag_id": fields.Int(),
    "description": fields.Str(),
    "status": fields.Str(),
})
def create_booking(mentee_id, slot_id, tag_id, description, status):
    try:
        booking_data = Booking.create(
            mentee_id=mentee_id,
            slot_id=slot_id,
            tag_id=tag_id,
            description=description,
            status=status,
        )
        return Response(
            json.dumps({
                "message": {booking_data.mentee_id, booking_data.slot_id, booking_data.tag_id, booking_data.description, booking_data.status}
            }),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


# update a booking
@blueprint.route("/api/bookings/booking", methods=["PUT", "PATCH"])
@check_token
@marshal_with(booking_schema)
@use_kwargs({
    "booking_id": fields.Int(),
    "mentee_id": fields.Int(),
    "slot_id": fields.Int(),
    "tag_id": fields.Int(),
    "description": fields.Str(),
    "status": fields.Str(),
})
def update_booking(booking_id, mentee_id, slot_id, tag_id, description, status):
    try:
        booking_data = Booking.query.filter(Booking.id==booking_id).first()
        booking_data.update(
            mentee_id=mentee_id,
            slot_id=slot_id,
            tag_id=tag_id,
            description=description,
            status=status,
        )
        booking_data.save()
        return booking_data
    except Exception as e:
        return {"message": str(e)}, 400


#  create a slot
@blueprint.route("/api/bookings/slot", methods=["POST"])
@check_token
@marshal_with(slot_schema)
@use_kwargs({
    "mentor_id": fields.Int(),
    "weekday_id": fields.Int,
    "start_time": fields.DateTime(),
    "duration": fields.Int(),
    "end_time": fields.DateTime(),
    "is_booked": fields.Int(),
})
def create_slot(mentor_id, weekday_id, start_time, duration, end_time, is_booked):
    try:
        slot_data = Slot.create(
            mentor_id=mentor_id,
            weekday_id=weekday_id,
            start_time=start_time,
            duration=duration,
            end_time=end_time,
            is_booked=is_booked,
        )
        return Response(
            json.dumps({
                "message": {slot_data.mentor_id, slot_data.weekday_id, slot_data.start_time, slot_data.duration, slot_data.end_time, slot_data.is_booked}
            }),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


# get slots
@blueprint.route("/api/bookings/slots", methods=["GET"])
@marshal_with(slot_schemas)
def get_slots():
    try:
        slot_data = Slot.query.all().order_by("created_at")
        return slot_data
    except Exception as e:
        return {"message": str(e)}, 400


# create weekday
@blueprint.route("/api/bookings/weekday", methods=["POST"])
@check_token
@marshal_with(weekday_schema)
@use_kwargs({"name": fields.Str()})
def create_weekday(name):
    try:
        weekday = WeekDay.create(
            name=name,
        )
        return Response(
            json.dumps({"message": weekday.name}),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


# get weekdays
@blueprint.route("/api/bookings/weekdays", methods=["GET"])
@marshal_with(weekday_schemas)
def get_weekdays():
    try:
        weekday_data = WeekDay.query.all().order_by("created_at")
        return weekday_data
    except Exception as e:
        return {"message": str(e)}, 400


# create service tag
@blueprint.route("/api/bookings/servicetag", methods=["POST"])
@check_token
@marshal_with(servicetag_schema)
@use_kwargs({"name": fields.Str()})
def create_tag(name):
    try:
        tag = ServiceTag.create(
            name=name,
        )
        return Response(
            json.dumps({"message": tag.name}),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


# get service tags
@blueprint.route("/api/bookings/servicetags", methods=["GET"])
@marshal_with(servicetag_schemas)
def get_tags():
    try:
        tag_data = ServiceTag.query.all().order_by("created_at")
        return tag_data
    except Exception as e:
        return {"message": str(e)}, 400