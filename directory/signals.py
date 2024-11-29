from celery import chain
from django.db.models.signals import post_save
from django.dispatch import receiver

from business.utils import broker_publish, abroker_publish
from directory.models import Profile
from directory.tasks import get_business_info
from location.models import Location
from messaging.models import Event

from messaging.tasks import prepare_notification


@receiver(post_save, sender=Profile)
async def on_profile_save(sender, instance, created, **kwargs):
    """
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """

    if created:
        Location.objects.acreate(name='HQ', address=instance.address, city=instance.city, contact=instance.contact,
                                 business_id=instance.pk)
        stream_data = {'user_identifier': instance.owner.__str__()}

        # broker_publish('user-data', stream_data)
        await abroker_publish('user-data', stream_data)

        chain(get_business_info.s(profile_id=instance.pk), prepare_notification.s(event=Event.Nb)).apply_async(
            countdown=2)
