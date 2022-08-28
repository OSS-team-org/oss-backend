from marshmallow import Schema, fields, pre_load, post_dump



class BookingSchema(Schema):
    id = fields.Integer()
    mentee_id = fields.Integer()
    slot_id = fields.Integer()
    tags = fields.Nested("TagSchema", many=True, dump_only=True)
    description = fields.String()
    status = fields.String(default="PENDING")
    is_confirmed = fields.Boolean()
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at")

    @pre_load
    def make_booking(self, data, **kwargs):
        return data

    @post_dump
    def dump_booking(self, data, **kwargs):
        return data

    class Meta:
        strict = True

booking_schema = BookingSchema()
booking_schemas = BookingSchema(many=True)


class SlotSchema(Schema):
    id = fields.Integer()
    mentor_id = fields.Integer()
    weekday_id = fields.Integer()
    start_time = fields.Time()
    duration = fields.Integer()
    end_time = fields.Time()
    is_booked = fields.Boolean()
    mentor = fields.Nested(
        "AccountSchema",dump_only=True
    )
    weekday = fields.Nested(
        "WeekDaySchema", dump_only=True
    )
    @pre_load
    def make_slot(self, data, **kwargs):
        return data

    @post_dump
    def dump_slot(self, data, **kwargs):
        return data

    class Meta:
        strict = True

slot_schema = SlotSchema()
slot_schemas = SlotSchema(many=True)


class WeekDaySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at")

    @pre_load
    def make_weekday(self, data, **kwargs):
        return data

    @post_dump
    def dump_weekday(self, data, **kwargs):
        return data

    class Meta:
        strict = True

weekday_schema = WeekDaySchema()
weekday_schemas = WeekDaySchema(many=True)


class TagSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime(attribute="created_at", dump_only=True)
    updated_at = fields.DateTime(attribute="updated_at")

    @pre_load
    def make_tag(self, data, **kwargs):
        return data

    @post_dump
    def dump_tag(self, data, **kwargs):
        return data

    class Meta:
        strict = True

tag_schema = TagSchema()
tag_schemas = TagSchema(many=True)


class TagAccountSchema(Schema):
    tag = fields.Nested('TagSchema', dump_only=True)

    @pre_load
    def make_tag_account(self, data, **kwargs):
        return data

    @post_dump
    def dump_tag_account(self, data, **kwargs):
        return data

    class Meta:
        strict = True

tagaccount_schema = TagSchema()
tagaccount_schemas = TagSchema(many=True)
