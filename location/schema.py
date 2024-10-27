import uuid

from ninja import ModelSchema

from location.models import Location


class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        exclude = ['id', ]


class AddLocationSchema(ModelSchema):
    class Meta:
        model = Location
        exclude = ['id', 'status', 'identifier']


class ChangeLocationStatusSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ['status']
