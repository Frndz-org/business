from typing import List

from celery import chain
from django.db import IntegrityError
from ninja import Router

from business.schema import Message
from directory.models import Industry, Profile
from directory.schema import IndustrySchema, BusinessSchema, AddBusiness, BusinessStatus, UpdateBusiness
from directory.tasks import get_business_info
from messaging.models import Event
from messaging.tasks import prepare_notification

router = Router(tags=['Directory'])


@router.get('/industries', auth=None, response={200: List[IndustrySchema]})
def list_industries(request):
    """
    Retrieve industries
    :param request:
    :return:
    """
    return Industry.objects.all()


@router.get('/businesses', response={200: List[BusinessSchema]})
def list_businesses(request, owner=''):
    """
    Retrieve list of businesses
    :param request:
    :param owner:
    :return:
    """
    if owner != '':
        return Profile.objects.filter(owner=owner)
    return Profile.objects.all()


@router.get('/businesses/{uuid:identifier}', response={200: BusinessSchema, 404: Message})
def get_business(request, identifier):
    """
    Get business profile
    :param request:
    :param identifier:
    :return:
    """
    try:
        return Profile.objects.get(identifier=identifier)

    except Profile.DoesNotExist:

        return 404, {"detail": "Business Not Found"}


@router.post('/businesses', response={201: Message, 400: Message, 404: Message})
def add_new_business(request, payload: AddBusiness, output=None):
    """
    Add a new business
    :param request:
    :param payload:
    :return:
    """
    try:
        industry = Industry.objects.get(identifier=payload.industry)

        payload.industry = industry

        print(f"Output: {output}")

        if output == 'id':
            profile = Profile.objects.create(**payload.dict(), owner=request.auth['id'])

            return 201, {'detail': "Business Added", 'id': profile.identifier.__str__()}

        Profile.objects.create(**payload.dict(), owner=request.auth['id'])

        return 201, {"detail": "Business Added"}

    except Industry.DoesNotExist:
        return 404, {"detail": "Unknown Industry"}

    except IntegrityError:
        return 400, {"detail": "A business exist with the information provided"}


@router.put('/businesses/{uuid:identifier}', response={200: Message, 400: Message, 404: Message})
def update_business(request, identifier, payload: UpdateBusiness):
    """
    Update business details
    :param request:
    :param identifier:
    :param payload:
    :return:
    """
    try:

        profile = Profile.objects.get(identifier=identifier, owner=request.auth['id'])

        profile.name = payload.name

        profile.tax_id = payload.tax_id

        profile.address = payload.address

        profile.city = payload.city

        profile.contact = payload.contact

        profile.country = payload.country

        profile.save()

        return 200, {"detail": "Business details updated"}

    except Industry.DoesNotExist:
        return 404, {"detail": "Unknown Industry"}

    except Profile.DoesNotExist:
        return 404, {"detail": "Business Not Found"}

    except IntegrityError:
        return 400, {"detail": "A business exist with the information provided"}


@router.patch('/businesses/{uuid:identifier}', response={200: Message, 400: Message, 404: Message})
def change_business_status(request, identifier, payload: BusinessStatus):
    """
    Change business status
    :param request:
    :param identifier:
    :param payload:
    :return:
    """
    try:

        profile = Profile.objects.get(identifier=identifier)

        profile.status = payload.status

        profile.save()

        if profile.status == Profile.STATUS.Ac:
            chain(get_business_info.s(profile_id=profile.pk), prepare_notification.s(event=Event.Ab)).apply_async(
                countdown=2)

        if profile.status == Profile.STATUS.Sup:
            chain(get_business_info.s(profile_id=profile.pk), prepare_notification.s(event=Event.Sb)).apply_async(
                countdown=2)

        return 200, {"detail": "Business status updated"}

    except Profile.DoesNotExist:

        return 404, {"detail": "Business Not Found"}
