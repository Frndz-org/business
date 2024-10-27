from typing import List

from django.db import IntegrityError
from ninja import Router

from business.schema import Message
from directory.models import Profile
from location.models import Location
from location.schema import LocationSchema, AddLocationSchema, ChangeLocationStatusSchema

router = Router(tags=['Locations'])


@router.get('{uuid:business_identifier}/locations', response={200: List[LocationSchema]})
def list_locations(request, business_identifier):
    """
    Retrieve Locations or Branches
    :param request:
    :param business_identifier:
    :return:
    """
    return Location.objects.filter(business__identifier=business_identifier)


@router.get('{uuid:business_identifier}/locations/{uuid:identifier}', response={200: LocationSchema, 404: Message})
def get_location(request, business_identifier, identifier):
    """
    Get location profile
    :param business_identifier:
    :param request:
    :param identifier:
    :return:
    """
    try:
        return Location.objects.get(business__identifier=business_identifier, identifier=identifier)

    except Location.DoesNotExist:

        return 404, {"detail": "Location Not Found"}


@router.post('{uuid:business_identifier}/locations', response={201: Message, 400: Message, 404: Message})
def add_new_location(request, business_identifier, payload: AddLocationSchema):
    """
    Add a new location
    :param business_identifier:
    :param request:
    :param payload:
    :return:
    """
    try:

        location_exists = Location.objects.filter(owner=business_identifier, name=payload.name).exists()

        if location_exists:
            raise IntegrityError

        business = Profile.objects.get(identifier=business_identifier)

        Location.objects.create(**payload.dict(), business=business)

        return 201, {"detail": "Location Added"}

    except IntegrityError:
        return 400, {"detail": "A location exist either with name or contact provided"}

    except Profile.DoesNotExist:
        return 400, {"detail": "Business not found"}


@router.put('{uuid:business_identifier}/locations/{uuid:identifier}',
            response={200: Message, 400: Message, 404: Message})
def update_location(request, business_identifier, identifier, payload: AddLocationSchema):
    """
    Update location details
    :param business_identifier:
    :param request:
    :param identifier:
    :param payload:
    :return:
    """
    try:

        location = Location.objects.get(identifier=identifier, business_identifier=business_identifier)

        location.name = payload.name

        location.address = payload.address

        location.city = payload.city

        location.contact = payload.contact

        location.save()

        return 200, {"detail": "Location details updated"}

    except Location.DoesNotExist:
        return 404, {"detail": "Location Not Found"}

    except IntegrityError:
        return 400, {"detail": "A location exist either with name or contact provided"}


@router.patch('{uuid:business_identifier}/locations/{uuid:identifier}',
              response={200: Message, 400: Message, 404: Message})
def change_location_status(request, business_identifier, identifier, payload: ChangeLocationStatusSchema):
    """
    Change location status
    :param business_identifier:
    :param request:
    :param identifier:
    :param payload:
    :return:
    """
    try:

        location = Location.objects.get(business_identifier=business_identifier, identifier=identifier)

        location.status = payload.status

        location.save()

        # if location.status == Location.STATUS.ACTIVE:
        #     chain(get_business_info.s(profile_id=profile.pk), prepare_notification.s(event=Event.Ab)).apply_async(
        #         countdown=2)
        #
        # if location.status == Location.STATUS.SUSPENDED:
        #     chain(get_business_info.s(profile_id=profile.pk), prepare_notification.s(event=Event.Sb)).apply_async(
        #         countdown=2)
        #
        # if location.status == Location.STATUS.DEACTIVATED:
        #     chain(get_business_info.s(profile_id=profile.pk), prepare_notification.s(event=Event.Sb)).apply_async(
        #         countdown=2)

        return 200, {"detail": "Location status updated"}

    except Location.DoesNotExist:

        return 404, {"detail": "Location Not Found"}
