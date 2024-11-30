import uuid

from ninja import ModelSchema

from directory.models import Industry, Profile


class IndustrySchema(ModelSchema):
    class Meta:
        model = Industry
        fields = ['name', 'identifier']


class BusinessSchema(ModelSchema):
    industry: str

    @staticmethod
    def resolve_industry(business):
        return business.identifier.__str__()

    class Meta:
        model = Profile
        exclude = ['updated', 'created', 'owner', 'industry', 'id', 'country']


class BusinessStatus(ModelSchema):
    class Meta:
        model = Profile
        fields = ['status']


class AddBusiness(ModelSchema):
    industry: uuid

    class Config(ModelSchema.Config):
        arbitrary_types_allowed = True

    class Meta:
        model = Profile
        exclude = ['updated', 'created', 'owner', 'id', 'identifier', 'status']


class UpdateBusiness(ModelSchema):
    class Meta:
        model = Profile
        exclude = ['updated', 'created', 'owner', 'id', 'identifier', 'status', 'industry']
