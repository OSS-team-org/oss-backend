from marshmallow import Schema, fields, pre_load, post_dump
from mentor.booking.models import Slot

class BookingSchema(Schema):
    mentee_id = fields.Integer()
    slot_id = fields.Integer(queryset=Slot.objects.filter(is_booked=False))
    tag_id = fields.Integer()
    description = fields.String()
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at")

    @pre_load
    def make_account(self, data, **kwargs):
        return data

    @post_dump
    def dump_account(self, data, **kwargs):
        return data

    class Meta:
        strict = True

booking_schema = BookingSchema()
booking_schemas = BookingSchema(many=True)


class SlotSchema(Schema):
    mentor_id = fields.Integer()
    weekday_id = fields.Integer()
    start_time = fields.DateTime()
    duration = fields.Integer()
    end_time = fields.DateTime()
    is_booked = fields.Boolean()
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at")

    @pre_load
    def make_account(self, data, **kwargs):
        return data

    @post_dump
    def dump_account(self, data, **kwargs):
        return data

    class Meta:
        strict = True

slot_schema = SlotSchema()
slots_schema = SlotSchema(many=True)


class WeekDaySchema(Schema):
    name = fields.String()
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at")

    @pre_load
    def make_account(self, data, **kwargs):
        return data

    @post_dump
    def dump_account(self, data, **kwargs):
        return data

    class Meta:
        strict = True

weekday_schema = WeekDaySchema()
weekdays_schema = WeekDaySchema(many=True)


class ServiceTagSchema(Schema):
    name = fields.String()
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at")

    @pre_load
    def make_account(self, data, **kwargs):
        return data

    @post_dump
    def dump_account(self, data, **kwargs):
        return data

    class Meta:
        strict = True

servicetag_schema = ServiceTagSchema()
servicetags_schema = ServiceTagSchema(many=True)
