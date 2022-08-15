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

from .models import Booking, Tag, Slot, TagAccount, WeekDay

from flask_restx import Api

from .serializers import (
    booking_schema,
    booking_schemas,
    slot_schema,
    slot_schemas,
    weekday_schema,
    weekday_schemas,
    tag_schemas
)

blueprint = Blueprint("booking", __name__, url_prefix="/api")
api = Api(blueprint, doc="/doc/")


@blueprint.route("/doc/bookings/bookings", methods=["GET"])
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


@blueprint.route("/doc/bookings/bookings/<int:booking_id>", methods=["GET"])
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


@blueprint.route("/doc/bookings/booking", methods=["POST"])
@check_token
@marshal_with(booking_schema)
@use_kwargs({
    "mentee_id": fields.Int(),
    "slot_id": fields.Int(),
    "tags": fields.List(),
    "description": fields.Str(),
    "status": fields.Str(),
    "created_at": fields.Date(),
    "updated_at": fields.Date()
})
def create_booking(mentee_id, slot_id, tags, description, status, created_at, updated_at):
    try:
        booking_data = Booking.create(
            mentee_id=mentee_id,
            slot_id=slot_id,
            tags=tags,
            description=description,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )
        return Response(
            json.dumps({
                "message": {
                    booking_data.mentee_id, 
                    booking_data.slot_id, 
                    booking_data.tags, 
                    booking_data.description, 
                    booking_data.status,
                    booking_data.created_at,
                    booking_data.updated_at
                }
            }),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


@blueprint.route("/doc/bookings/booking", methods=["PUT", "PATCH"])
@check_token
@marshal_with(booking_schema)
@use_kwargs({
    "booking_id": fields.Int(),
    "mentee_id": fields.Int(),
    "slot_id": fields.Int(),
    "tag_id": fields.Int(),
    "description": fields.Str(),
    "status": fields.Str(),
    "updated_at": fields.Date()
})
def update_booking(booking_id, mentee_id, slot_id, tags, description, status, updated_at):
    try:
        booking_data = Booking.query.filter(Booking.id==booking_id).first()
        booking_data.update(
            mentee_id=mentee_id,
            slot_id=slot_id,
            tag_id=tags,
            description=description,
            status=status,
            updated_at=updated_at,
        )
        booking_data.save()
        return booking_data
    except Exception as e:
        return {"message": str(e)}, 400


@blueprint.route("/doc/bookings/slot", methods=["POST"])
@check_token
@marshal_with(slot_schema)
@use_kwargs({
    "mentor_id": fields.Int(),
    "weekday_id": fields.Int,
    "start_time": fields.DateTime(),
    "duration": fields.Int(),
    "end_time": fields.DateTime(),
    "is_booked": fields.Int(),
    "created_at": fields.Date(),
    "updated_at": fields.Date()
})
def create_slot(mentor_id, weekday_id, start_time, duration, end_time, is_booked, created_at, updated_at):
    try:
        slot_data = Slot.create(
            mentor_id=mentor_id,
            weekday_id=weekday_id,
            start_time=start_time,
            duration=duration,
            end_time=end_time,
            is_booked=is_booked,
            created_at=created_at,
            updated_at=updated_at,
        )
        return Response(
            json.dumps({
                "message": {
                    slot_data.mentor_id, 
                    slot_data.weekday_id, 
                    slot_data.start_time, 
                    slot_data.duration, 
                    slot_data.end_time, 
                    slot_data.is_booked,
                    slot_data.created_at,
                    slot_data.updated_at
                }
            }),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


@blueprint.route("/doc/bookings/slots", methods=["GET"])
@marshal_with(slot_schemas)
def get_slots():
    try:
        slot_data = Slot.query.all().order_by("created_at")
        return slot_data
    except Exception as e:
        return {"message": str(e)}, 400


@blueprint.route("/doc/bookings/weekday", methods=["POST"])
@check_token
@marshal_with(weekday_schema)
@use_kwargs({"name": fields.Str(), "created_at": fields.Date(), "updated_at": fields.Date()})
def create_weekday(name, created_at, updated_at):
    try:
        weekday = WeekDay.create(
            name=name,
            created_at=created_at,
            updated_at=updated_at,
        )
        return Response(
            json.dumps({"message": {weekday.name, weekday.created_at, weekday.updated_at}}),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


@blueprint.route("/doc/bookings/weekdays", methods=["GET"])
@marshal_with(weekday_schemas)
def get_weekdays():
    try:
        weekday_data = WeekDay.query.all().order_by("created_at")
        return weekday_data
    except Exception as e:
        return {"message": str(e)}, 400


@blueprint.route("/doc/bookings/tag-account", methods=["POST"])
@check_token
@use_kwargs({"name": fields.Str(), "created_at": fields.Date(), "updated_at": fields.Date()})
def create_tag_account(name, created_at, updated_at, booking_id):
    try:
        tag = Tag(
            name=name,
            created_at=created_at,
            updated_at=updated_at,
        )
        tag.save()
        tag_account = TagAccount(
            booking_id=booking_id,
            tag_id=tag.id
        )
        tag_account.save()
        return Response(
            json.dumps({"message": {tag.name, tag.created_at, tag.updated_at, tag_account.booking_id, tag_account.tag_id}}),
            status=201,
            mimetype="application/json"
        )
    except Exception as e:
        return {"message": str(e)}, 400


@blueprint.route("/doc/bookings/tags", methods=["GET"])
@marshal_with(tag_schemas)
def get_tags():
    try:
        tag_data = Tag.query.all().order_by("created_at")
        return tag_data
    except Exception as e:
        return {"message": str(e)}, 400
